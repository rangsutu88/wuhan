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
import requests
import json

from lch.zhulong import est_tbs, est_meta, est_html, est_gg


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='jinggangshan'

def f1(driver,num):
    vw_class_dict={
        'zfcggg':'vw_class_container510989586913',
        'jsgcgg':'vw_class_container704506123991',
        'xeyxgcgg':'vw_class_container972030964765',
        'jgs-zbgs':'vw_class_container092363484519',
    }

    locator = (By.XPATH, "//div[@class='list2']/span/ul/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page_all = driver.find_element_by_xpath("//div[@class='list2']/span").text
    cnum = re.findall('页次：(\d+)/', page_all)[0]
    url=driver.current_url
    mark=re.findall('html/(.+)/index.html',url)[0]

    if int(cnum) != num:

        val = driver.find_element_by_xpath("//div[@class='list2']/span/ul/li[1]/a").get_attribute('href').rsplit('/',maxsplit=1)[1]

        driver.execute_script("""
        function goClass_page(){
        currentPageNo.val(%s);
        pubPostAjax('/frontDialogClassNewsList_getClassNews','%s','');
        }
        num=10
        goClass_page()
        """%(num,vw_class_dict[mark]))

        locator = (By.XPATH, "//div[@class='list2']/span/ul/li[1]/a[not(contains(@href,'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    data=[]

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find('div', class_='list2')
    span = tables.find('span')
    lis = span.find_all('li')
    for li in lis:
        href = li.a['href']
        if 'http' in href:
            href = href
        else:
            href = 'http://jgszb.jgs.gov.cn' + href
        ggstart_time = li.span.get_text().strip()
        name = li.a.get_text().strip()
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df




def f2(driver):

    locator = (By.XPATH, "//div[@class='list2']/span/ul/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page_all = driver.find_element_by_xpath("//div[@class='list2']/span").text
    total = re.findall('/(\d+)页', page_all)[0]
    total=int(total)

    driver.quit()

    return total

def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="article_show"]')

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
    div = soup.find('li',id="zoom")

    return div



data=[
    ["gcjs_gg","http://jgszb.jgs.gov.cn/html/jsgcgg/index.html",['name','ggstart_time','href','info'],f1,f2],

    ["zfcg_gg", "http://jgszb.jgs.gov.cn/html/zfcggg/index.html",["name", "ggstart_time", "href",'info'],f1,f2],

    ["qita_gg", "http://jgszb.jgs.gov.cn/html/xeyxgcgg/index.html",["name", "ggstart_time", "href",'info'],f1,f2],

    ["zhongbiao_gg", "http://jgszb.jgs.gov.cn/html/jgs-zbgs/index.html",["name", "ggstart_time", "href",'info'],f1,f2],

]

def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省井冈山市",**args)
    est_html(conp,f=f3,**args)



if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","jiangxi","jinggangshan"]

    work(conp=conp)