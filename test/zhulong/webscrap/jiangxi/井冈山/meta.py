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

from  lmfscrap import web

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



def f1(driver,num):
    # print('正在爬{}页'.format(num))
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
        ggstart_time = li.span.get_text()
        name = li.a.get_text()
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    print('*******************************完成{}页******************************'.format(num))
    return df




def f2(driver):

    locator = (By.XPATH, "//div[@class='list2']/span/ul/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page_all = driver.find_element_by_xpath("//div[@class='list2']/span").text
    total = re.findall('/(\d+)页', page_all)[0]
    total=int(total)

    driver.quit()

    return total



def general_template(tb,url,col,conp):

    m=web()
    setting={
    "url":url,
    "f1":f1,
    "f2":f2,
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":1,
    # 'total':10



    }
    m=web()
    m.write(**setting)

def work(conp,i=-1):
    data=[
    # ["gcjs_gg","http://jgszb.jgs.gov.cn/html/jsgcgg/index.html",['name','ggstart_time','href']],

    # ["zfcg_gg", "http://jgszb.jgs.gov.cn/html/zfcggg/index.html",["name", "ggstart_time", "href"]],

    ["qita_gg", "http://jgszb.jgs.gov.cn/html/xeyxgcgg/index.html",["name", "ggstart_time", "href"]],

    # ["zhongbiao_gg", "http://jgszb.jgs.gov.cn/html/jgs-zbgs/index.html",["name", "ggstart_time", "href"]],

    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)

# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","jinggangshan"]

work(conp=conp)