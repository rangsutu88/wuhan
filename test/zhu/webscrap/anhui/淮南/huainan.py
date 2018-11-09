import pandas as pd  
import re 

from selenium import webdriver 
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

import sys 
import time

import json
from zhulong.util.etl import gg_meta,gg_html



# driver=webdriver.Chrome()

# url="""http://jyzx.yiyang.gov.cn/jyxx/003001/003001001/2.html"""

# driver.get(url)


def f1(driver,num):

    locator = (By.XPATH, '//li[@class="ewb-info-item"][1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    main_url = url.rsplit('=', maxsplit=1)[0]

    cnum=re.findall(r'Paging=(\d+)',url)[0]

    if cnum != str(num):

        url=main_url + '='+str(num)
        val = driver.find_element_by_xpath('//li[@class="ewb-info-item"][1]/a').text
        driver.get(url)

        # 第二个等待
        locator = (
        By.XPATH, '//li[@class="ewb-info-item"][1]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.find_all('li', class_='ewb-info-item')

    for tr in lis:

        href = tr.a['href']
        name = tr.a['title']
        ggstart_time = tr.span.get_text()
        if 'http' in href:
            href = href
        else:
            href = 'http://www.hnsztb.cn' + href

        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df=pd.DataFrame(data=data)

    df["info"]=None
    return df 


def f2(driver):
    locator = (By.XPATH, '//li[@class="ewb-info-item"][1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//td[@class="huifont"]').text

    total = re.findall('/(\d+)', page)[0]
    total = int(total)

    driver.quit()
    return total


def f3(driver,url):
    driver.get(url)

    locator = (By.XPATH, '/html/body/div[3]/div[2]/div/div/div/table/tbody/tr[4]/td')

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

    div = soup.find('div', attrs={'id': re.compile('menutab_5_\d'), 'style': ''})
    
    return div






data=[
    ["gcjs_zhaobiao_gg_sbj","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001001/002001001001/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhaobiao_gg_sx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001001/002001001002/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhaobiao_gg_ftx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001001/002001001003/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_dayibiangeng_gg_sbj","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001003/002001003002/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_dayibiangeng_gg_sx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001003/002001003001/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_dayibiangeng_gg_ftx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001003/002001003001/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_zhongbiaohx_gg_sbj","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001004/002001004003/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg_sx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001004/002001004001/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg_ftx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001004/002001004002/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_zhongbiao_gg_sbj","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001002/002001002001/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg_sx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001002/002001002002/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg_ftx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001002/002001002003/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["gcjs_gg_sx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001005/002001005002/?Paging=1",["name","ggstart_time","href","info"],f1,f2],


    ["zfcg_zhaobiao_gg_sbj","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002001/002002001001/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhaobiao_gg_sx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002001/002002001002/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhaobiao_gg_ftx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002001/002002001003/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiaodyx_gg_sbj","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002006/002002006001/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhaobiaodyx_gg_sx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002006/002002006002/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhaobiaodyx_gg_ftx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002006/002002006003/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhongbiao_gg_sbj","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002002/002002002001/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg_sx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002002/002002002002/?Paging=1",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg_ftx","http://www.hnsztb.cn/HNWeb_NEW/jyxx/002002/002002002/002002002003/?Paging=1",["name","ggstart_time","href","info"],f1,f2],

    #政府采购答疑变更未爬


]

def work(conp):
    gg_meta(conp,data=data,diqu="安徽省淮南市")

    gg_html(conp,f=f3)


work(conp=["postgres","since2015","192.168.3.171","anhui","huainan"])

