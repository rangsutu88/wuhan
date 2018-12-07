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

_name_="yichun"

def f1(driver,num):
    locator=(By.XPATH,"//tr[@class='tdLine'][1]/td/a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    if "index.htm" in url:
        cnum=1
    else:
        cnum=int(re.findall("index_([0-9]{1,}).html",url)[0])+1
    if num!=cnum:
        if num==1:
            url=re.sub("index[_0-9]*.html","index.html",url)
        else:
            s="index_%d.html"%(num-1) if num>1 else "index.html"
            url=re.sub("index[_0-9]*.html",s,url)
        val=driver.find_element_by_xpath("//tr[@class='tdLine'][1]/td/a").text
        driver.get(url)
        locator=(By.XPATH,"//tr[@class='tdLine'][1]/td/a[not(contains(string(),'%s'))]"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find_all('tr', class_='tdLine')
    data = []
    url = driver.current_url
    rindex = url.rfind('/')
    main_url = url[:rindex]
    for tr in trs:
        tds = tr.find_all('td')
        href = tds[0].a['href'].strip('.')
        name = tds[0].a['title']
        ggstart_time = tds[1].get_text().strip()

        if re.findall('http', href):
            href = href
        else:
            href = main_url + href
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, "//tr[@class='tdLine'][1]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//a[@class="clz1"][last()]').get_attribute('href')
    total = re.findall(r'index_(\d+).htm', page)[0]
    total=int(total)+1
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '/html/body/table[2]/tbody/tr/td[3]/table[2]')

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
    div = soup.find('td',class_='NewsContent')
    return div

data=[
    #
    ["gcjs_zhao_gg","http://www.ycztbw.gov.cn/zbgg/jsgc_5751/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhao_gg","http://www.ycztbw.gov.cn/zbgg/zfcg_5755/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_jiaotong_zhao_gg","http://www.ycztbw.gov.cn/zbgg/gljt_5752/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_shuili_zhao_gg","http://www.ycztbw.gov.cn/zbgg/slgc_5753/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_yuanlin_zhao_gg","http://www.ycztbw.gov.cn/zbgg/szyl_5754/index.html",["name","ggstart_time","href",'info'],f1,f2],
    #
    ["gcjs_zhong_gg","http://www.ycztbw.gov.cn/zbgs/jsgc_5759/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_shuili_zhong_gg","http://www.ycztbw.gov.cn/zbgs/slgc_5761/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_yuanlin_zhong_gg","http://www.ycztbw.gov.cn/zbgs/szyl_5762/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhong_gg","http://www.ycztbw.gov.cn/zbgs/zfcg_5763/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_jiaotong_zhong_gg", "http://www.ycztbw.gov.cn/zbgs/gljt_5760/index.html",["name", "ggstart_time", "href",'info'],f1,f2],


]
def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省宜春市",**args)
    est_html(conp,f=f3,**args)
    # est_gg(conp,diqu="江西省宜春市")

if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","jiangxi","yichun"]

    work(conp=conp)