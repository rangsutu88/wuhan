import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from zhulong.util.etl import est_tbs,est_meta,est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



def f1(driver,num):
    locator=(By.XPATH,"//table[@class='bg'][1]/tbody/tr/td/a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    if "index.htm" in url:
        cnum=1
    else:
        cnum=int(re.findall("index_([0-9]{1,}).htm",url)[0])+1
    if num!=cnum:
        if num==1:
            url=re.sub("index[_0-9]*.htm","index.htm",url)
        else:
            s="index_%d.htm"%(num-1) if num>1 else "index.htm"
            url=re.sub("index[_0-9]*.htm",s,url)
        val=driver.find_element_by_xpath("//table[@class='bg'][1]/tbody/tr/td/a").text
        driver.get(url)
        locator=(By.XPATH,"//table[@class='bg'][1]/tbody/tr/td/a[not(contains(string(),'%s'))]"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))


    rindex = url.rfind('/')
    main_url = url[:rindex]

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    data=[]
    tables = soup.find_all('table', class_='bg')
    for table in tables:
        tds = table.find_all('td')
        name = tds[0].a['title']
        href = tds[0].a['href']
        ggstart_time = tds[1].get_text()

        if re.findall('http', href):
            href = href
        elif re.findall('\.\.\/\.\.',href):

            href = 'http://www.fzztb.gov.cn/'+href.strip(r'../..')

        else:
            href=main_url+href.strip(r'.')

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, "//table[@class='bg'][1]/tbody/tr/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath("(//*[@class='cy05'])[last()]").get_attribute('href')
    total = 0 if re.findall(r'index_(\d+).htm', page) ==[] else re.findall(r'index_(\d+).htm', page)[0]
    total=int(total)+1
    driver.quit()
    return total



def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '/html/body/table[2]/tbody/tr/td/table[3]')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')
    div = soup.find('td',id='Zoom2')
    return div

data=[

    ["gcjs_zhaobiao_gg","http://www.fzztb.gov.cn/jsgc/zbgg/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_zhongbiaohx_yaoqing_gg","http://www.fzztb.gov.cn/jsgc/zbgs/gkzb/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_zhongbiaohx_gongkai_gg","http://www.fzztb.gov.cn/jsgc/zbgs/yqzb/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_liubiao_gg","http://www.fzztb.gov.cn/jsgc/lbgs/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_xianjixingxi_gg","http://www.fzztb.gov.cn/jsgc/xjxx/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    #
    #
    ["zfcg_zhaobiao_gongkai_gg","http://www.fzztb.gov.cn/zfcg/zbgg/gkzb/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_xianjixingxi_gg","http://www.fzztb.gov.cn/zfcg/xjxx/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_liubiao_gg","http://www.fzztb.gov.cn/zfcg/lbgs/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.fzztb.gov.cn/zfcg/zbgs/index.htm",["name","ggstart_time","href",'info'],f1,f2],




    ["zfcg_zhaobiao_tanpan_gg","http://www.fzztb.gov.cn/zfcg/zbgg/jzxtp/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhaobiao_danyilaiyuan_gg","http://www.fzztb.gov.cn/zfcg/zbgg/dyxly/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhaobiao_cuoshang_gg","http://www.fzztb.gov.cn/zfcg/zbgg/jzxcs/index.htm",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhaobiao_yaoqing_gg","http://www.fzztb.gov.cn/zfcg/zbgg/yqzb/index.htm",["name","ggstart_time","href",'info'],f1,f2],

    ["zfcg_zhaobiao_xunjia_gg","http://www.fzztb.gov.cn/zfcg/zbgg/xj/index.htm",["name","ggstart_time","href",'info'],f1,f2],


]
def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省抚州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    # conp=["testor","zhulong","192.168.3.171","test","lch"]
    # conp=["testor","zhulong","192.168.3.171","test","public"]
    conp=["postgres","since2015","192.168.3.171","jiangxi","fuzhou"]

    work(conp=conp)