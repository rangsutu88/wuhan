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
    locator = (By.XPATH, '//div[@class="ewb-left-menu"]/ul/li[2]/div[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    driver.find_element_by_xpath('//div[@class="ewb-left-menu"]/ul/li[2]/div[1]/a').click()

    time.sleep(3)


    try:
        input = driver.find_element_by_xpath('//*[@id="003004007"]')
        print(input)
        input.click()
    except:
        input = driver.find_element_by_xpath('//*[@id="003004007"]')
        print(input)
        input.click()

    time.sleep(3)
    driver.find_element_by_class_name('pg_num_input').clear()
    driver.find_element_by_class_name('pg_num_input').send_keys(num)
    try:
        driver.find_element_by_class_name('pg_gobtn').click()
    except:
        driver.find_element_by_class_name('pg_gobtn').click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, '//*[@id="xxList"]/tr[1]/td[1]'), str((int(num) - 1) * 15 + 1)))

    page=driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find('tbody', id='xxList')
    trs = table.find_all('tr')
    data = []
    for i in trs:
        # tmp=[]
        tds = i.find_all('td')
        pro_method = tds[2].string
        tran_method = tds[3].string
        href = tds[4].find('a')['href']
        href = 'http://ggzyjy.ntzw.gov.cn' + href
        items_name = tds[4].get_text()
        address = tds[5].get_text().strip()
        add_time = tds[6].get_text().strip()

        tmp = [pro_method, tran_method, href, items_name, address, add_time]

        data.append(tmp)
    print(data)
    df = pd.DataFrame(data=data)


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
    
