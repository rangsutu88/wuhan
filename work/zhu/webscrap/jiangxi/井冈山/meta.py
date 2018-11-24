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

from zhulong.util.etl import est_tbs, est_meta, est_html, est_gg


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



def f1(driver,num):

    locator = (By.XPATH, "//div[@class='list2']/span/ul/li[1]/a")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

    while True:

        page_all = driver.find_element_by_xpath("//div[@class='list2']/span").text
        page = re.findall('页次：(\d+)/', page_all)[0]

        if int(page)==num:
            break

        if int(page) > num:
            if int(page)-num>10:
                for _ in range((int(page)-num)//2):
                    driver.execute_script("goClass_previousPage();")
                    time.sleep(1)
            val = driver.find_element_by_xpath("//div[@class='list2']/span/ul/li[1]/a").text
            driver.execute_script("goClass_previousPage();")
            try:
                locator = (By.XPATH, "//div[@class='list2']/span/ul/li[1]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                time.sleep(1)
        if int(page) < num:
            if num-int(page)>10:
                for _ in range((num-int(page))//2):
                    driver.execute_script("goClass_nextPage();")
                    time.sleep(1)
            val = driver.find_element_by_xpath("//div[@class='list2']/span/ul/li[1]/a").text
            driver.execute_script("goClass_nextPage();")
            try:
                locator = (By.XPATH, "//div[@class='list2']/span/ul/li[1]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                time.sleep(1)

        if abs(int(page)-num)>21:
            val = driver.find_element_by_xpath("//div[@class='list2']/span/ul/li[1]/a").text
            driver.execute_script("goClass_lastPage();")
            try:
                locator = (By.XPATH, "//div[@class='list2']/span/ul/li[1]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                time.sleep(1)

    data=[]
    # print('doing{}'.format(num))
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
    # est_gg(conp,diqu="江西省井冈山市")


if __name__=='__main__':

    # conp=["testor","zhulong","192.168.3.171","test","lch"]
    # conp=["testor","zhulong","192.168.3.171","test","public"]
    conp=["postgres","since2015","192.168.3.171","jiangxi","jinggangshan"]

    work(conp=conp)