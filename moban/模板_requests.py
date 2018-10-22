import time

import pandas as pd
import re

import requests
from selenium import webdriver 
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import json

from  lmfscrap import web

# __conp=["postgres","since2015","192.168.3.171","hunan","zhuzhou"]


# url="http://www.zzzyjy.cn/016/016001/1.html"
# # # driver=webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


def f1(driver,num):
    cookie = driver.get_cookies()
    cookies = {}
    for i in cookie:
        cookies['{}'.format(i['name'])] = i['value']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',

    }

    req = requests.get(url='http://ggzyjy.ntzw.gov.cn/services/XzsJsggWebservice/'
                           'getList?response=application/json&pageIndex={page}&'
                           'pageSize=15&&categorynum=003004007&diqu2=&xmlx=&xmmc='.format(page=num),
                       headers=headers, cookies=cookies, timeout=4)
    data = []
    con = req.json()
    ret = con['return']
    ret = json.loads(ret)
    tables = ret['Table']
    for table in tables:
        href = table['href']
        href = 'http://ggzyjy.ntzw.gov.cn' + href
        rindex = table['title'].rfind(']')
        title = table['title']


        rindex = str.rfind(']')
        str = str[rindex + 1:]
        jyfl = table['jyfl']
        city = table['city']
        jyfs = table['jyfs']
        postdate = table['postdate']

        tmp = [jyfl, jyfs, title, href, city, postdate]
        data.append(tmp)

    df = pd.DataFrame(data=data)
    return df


def f2(driver):
    locator=(By.XPATH,'//div[@class="ewb-left-menu"]/ul/li[2]/div[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    driver.find_element_by_xpath('//div[@class="ewb-left-menu"]/ul/li[2]/div[1]/a').click()
    time.sleep(1)
    locator=(By.XPATH,'//*[@id="divInfoReportPage"]/span[4]')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    page_all=driver.find_element_by_xpath('//*[@id="divInfoReportPage"]/span[4]').text
    driver.find_element_by_xpath('//*[@id="003004007"]').click()
    if "下页" in driver.page_source:
        locator=(By.XPATH,'//*[@id="divInfoReportPage"]/span[4]')
        WebDriverWait(driver,20).until_not(EC.text_to_be_present_in_element(locator,page_all))
        total=int(driver.find_element_by_class_name("pg_maxpagenum").text.split('/')[1])

        driver.quit()
        return total
    else:
        driver.quit()
        return 1


def general_template(tb,url,col,conp):

    m=web()
    setting={
    "url":url,
    "f1":f1,
    "f2":f2,
    "tb":tb,#数据库名
    "col":col,#数据库字段名
    "conp":conp,
    "num":1,



    }
    m=web()
    m.write(**setting)

def work(conp,i=-1):

    data=[
        ["jsnt_zhenfu_caigou_gg","http://ggzyjy.ntzw.gov.cn/jyxx/tradeInfo.html",["pro_method","tran_method","items_name","href","address","add_time"]],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)

conp=["testor","zhulong","192.168.3.171","test","public"]

work(conp=conp,i=0)
    
