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


from zhulong.util.etl import est_tbs, est_meta, est_html, est_gg


# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='jiangxi'


def f1(driver,num):
    try:
        locator = (By.XPATH, '//*[@id="gengerlist"]/div[1]/ul/li[1]/a')
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
    except:
        title = driver.title
        if title == '404 Not Found':
            return
        else:
            locator = (By.XPATH, '//*[@id="gengerlist"]/div[1]/ul/li[1]/a')
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    cnum=int(re.findall("/([0-9]{1,}).html",url)[0])

    if num!=cnum:
        s="/%d.html"%(num)
        url=re.sub("/[0-9]{1,}.html",s,url)
        val=driver.find_element_by_xpath('//*[@id="gengerlist"]/div[1]/ul/li[1]/a').text

        driver.get(url)

        try:
            locator=(By.XPATH,"//*[@id='gengerlist']/div[1]/ul/li[1]/a[not(contains(string(),'%s'))]"%val)
            WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
        except:
            title = driver.title
            if title == '404 Not Found':
                return
            else:
                locator = (By.XPATH, "//*[@id='gengerlist']/div[1]/ul/li[1]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

    ht = driver.page_source
    soup = BeautifulSoup(ht, 'lxml')
    uls = soup.find('div', class_="ewb-infolist")
    lis = uls.find_all('li')
    data=[]
    for li in lis:
        name = li.a.get_text()
        href = li.a['href']
        href = 'http://www.jxsggzy.cn' + href
        ggstart_time = li.span.get_text()
        tmp = [name, ggstart_time,href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):

    locator = (By.XPATH, '//*[@id="gengerlist"]/div[1]/ul/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    try:
        total=int(driver.find_element_by_xpath('//*[@id="index"]').text.split('/')[1])
    except:
        total=1

    driver.quit()
    return total

def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="article-info"]')

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
    div = soup.find('div',class_="con")
    return div



data=[

    ["gcjs_fangwushizheng_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002001/002001001/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_fangwushizheng_dayi_gg","http://www.jxsggzy.cn/web/jyxx/002001/002001002/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_fangwushizheng_zhongbiaohx_gg","http://www.jxsggzy.cn/web/jyxx/002001/002001004/1.html",["name","ggstart_time","href",'info'],f1,f2],

    ["gcjs_jiaotong_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002002/002002002/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_jiaotong_buyi_gg","http://www.jxsggzy.cn/web/jyxx/002002/002002003/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_jiaotong_zhongbiaohx_gg","http://www.jxsggzy.cn/web/jyxx/002002/002002005/1.html",["name","ggstart_time","href",'info'],f1,f2],

    ["gcjs_shuili_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002003/002003001/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_shuili_dayi_gg","http://www.jxsggzy.cn/web/jyxx/002003/002003002/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_shuili_zhongbiaohx_gg","http://www.jxsggzy.cn/web/jyxx/002003/002003004/1.html",["name","ggstart_time","href",'info'],f1,f2],

    ["gcjs_zhongdian_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002005/002005001/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_zhongdian_dayi_gg","http://www.jxsggzy.cn/web/jyxx/002005/002005002/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_zhongdian_zhongbiaohx_gg","http://www.jxsggzy.cn/web/jyxx/002005/002005004/1.html",["name","ggstart_time","href",'info'],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002006/002006001/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_biangen_gg","http://www.jxsggzy.cn/web/jyxx/002006/002006002/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_dayi_gg","http://www.jxsggzy.cn/web/jyxx/002006/002006003/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.jxsggzy.cn/web/jyxx/002006/002006004/1.html",["name","ggstart_time","href",'info'],f1,f2],

    ["yycg_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002010/002010001/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["yycg_zhongbiao_gg","http://www.jxsggzy.cn/web/jyxx/002010/002010002/1.html",["name","ggstart_time","href",'info'],f1,f2],

    ["qita_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002013/002013001/1.html",["name","ggstart_time","href",'info'],f1,f2],
    ["qita_zhongbiao_gg","http://www.jxsggzy.cn/web/jyxx/002013/002013002/1.html",["name","ggstart_time","href",'info'],f1,f2],

    ["zfcg_zhaobiao_dyxly_gg","http://www.jxsggzy.cn/web/jyxx/002006/002006005/1.html",["name","ggstart_time","href",'info'],f1,f2],


]

def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省江西",**args)
    est_html(conp,f=f3,**args)
    # est_gg(conp,diqu="江西省江西")


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","jiangxi","jiangxi"]

    work(conp=conp)