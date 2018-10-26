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
    locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page=driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/div[1]/font[3]/b').text

    if int(page) != num:
        val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))
        try:
            locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]'%val)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(locator))
        except:
            locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' %val)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(locator))


    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', id='MoreInfoList1_DataGrid1')
    trs = table.find_all('tr')
    data=[]
    for tr in trs:
        tds = tr.find_all('td')
        href = tds[1].a['href']
        href = 'http://www.xyggzy.cn' + href
        title = tds[1].a['title']
        date_time = tds[2].get_text().strip()
        tmp = [title,date_time,href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    # print('完成{}页'.format(num))
    return df




def f2(driver):

    locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    total = driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/div[1]/font[2]/b').text
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
    "num":5,
    # 'total':5



    }
    m=web()
    m.write(**setting)

def work(conp,i=-1):
    data=[
    ["gcjs_zhaobiao_gg","http://www.xyggzy.cn/ggzy/jsgc/010001/MoreInfo.aspx?CategoryNum=010001",['name','ggstart_time','href']],
    ["gcjs_zhongbiaohx_gg","http://www.xyggzy.cn/ggzy/jsgc/010002/MoreInfo.aspx?CategoryNum=010002",['name','ggstart','href']],

        ["zfcg_zhaobiao_gg", "http://www.xyggzy.cn/ggzy/zfcg/009001/MoreInfo.aspx?CategoryNum=009001",["name", "ggstart_time", "href"]],
        ["zfcg_zhongbiaohx_gg", "http://www.xyggzy.cn/ggzy/zfcg/009002/MoreInfo.aspx?CategoryNum=009002",["name", "ggstart_time", "href"]],

    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)

# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","xinyu"]

work(conp=conp)