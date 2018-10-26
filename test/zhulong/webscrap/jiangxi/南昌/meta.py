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
    print('正在爬{}页'.format(num))
    locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page=driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text

    if int(page) != num:
        val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))
        try:
            locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]'%val)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(locator))
        except:
            locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(locator))


    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', id='MoreInfoList1_DataGrid1')
    trs = table.find_all('tr')
    data=[]
    for tr in trs:
        tds = tr.find_all('td')
        href = tds[1].a['href']
        href = 'http://ncztb.nc.gov.cn' + href
        title = tds[1].a['title']
        date_time = tds[2].get_text().strip()
        tmp = [title, date_time,href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    print('完成{}页'.format(num))
    return df




def f2(driver):

    locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    total = driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text
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
    "num":10,
    # 'total':5



    }
    m=web()
    m.write(**setting)

def work(conp,i=-1):
    data=[
    ["gcjs_fangjianshizheng_zhaobiao_gg","http://ncztb.nc.gov.cn/nczbw/jyxx/002001/002001002/MoreInfo.aspx?CategoryNum=002001002",['name','ggstart_time','href']],
    ["gcjs_fangjianshizheng_dayi_gg","http://ncztb.nc.gov.cn/nczbw/jyxx/002001/002001004/MoreInfo.aspx?CategoryNum=002001004",['name','ggstart_time','href']],
    ["gcjs_fangjianshizheng_zhongbiaohx_gg","http://ncztb.nc.gov.cn/nczbw/jyxx/002001/002001005/MoreInfo.aspx?CategoryNum=002001005",['title','ggstart_time','href']],

    ["gcjs_jiaotong_zhaobiao_gg","http://ncztb.nc.gov.cn/nczbw/jyxx/002002/002002002/MoreInfo.aspx?CategoryNum=002002002",["name", "ggstart_time", "href"]],

    ["gcjs_jiaotong_zhongbiao_gg","http://ncztb.nc.gov.cn/nczbw/jyxx/002002/002002005/MoreInfo.aspx?CategoryNum=002002005",["name", "ggstart_time", "href"]],

        ["gcjs_shuili_zhaobiao_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002003/002003001/MoreInfo.aspx?CategoryNum=002003001",["name", "ggstart_time", "href"]],
        ["gcjs_shuili_zhongbiaohx_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002003/002003004/MoreInfo.aspx?CategoryNum=002003004",["name", "ggstart_time", "href"]],



        ["gcjs_tielu_zhaobiao_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002009/002009001/MoreInfo.aspx?CategoryNum=002009001",["name", "ggstart_time", "href"]],
        ["gcjs_tielu_zhongbiao_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002009/002009004/MoreInfo.aspx?CategoryNum=002009004",["name", "ggstart_time", "href"]],



        ["gcjs_zhongdian_zhaobiao_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002010/002010001/MoreInfo.aspx?CategoryNum=002010001",["name", "ggstart_time", "href"]],
        ["gcjs_zhongdian_dayi_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002010/002010002/MoreInfo.aspx?CategoryNum=002010002",["name", "ggstart_time", "href"]],
        ["gcjs_zhongdian_zhongbiaohx_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002010/002010004/MoreInfo.aspx?CategoryNum=002010004",["name", "ggstart_time", "href"]],



        ["zfcg_zhaobiao_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002004/002004001/MoreInfo.aspx?CategoryNum=002004001",["name", "ggstart_time", "href"]],
        ["zfcg_biangeng_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002004/002004002/MoreInfo.aspx?CategoryNum=002004002",["name", "ggstart_time", "href"]],
        ["zfcg_dayi_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002004/002004003/MoreInfo.aspx?CategoryNum=002004003", ["name", "ggstart_time", "href"]],
        ["zfcg_zhongbiao_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002004/002004004/MoreInfo.aspx?CategoryNum=002004004",["name", "ggstart_time", "href"]],

        ["yycg_zhaobiao_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002011/002011001/MoreInfo.aspx?CategoryNum=002011001",["name", "ggstart_time", "href"]],
        ["yycg_zhongbiao_gg", "http://ncztb.nc.gov.cn/nczbw/jyxx/002011/002011002/MoreInfo.aspx?CategoryNum=002011002",["name", "ggstart_time", "href"]],

    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)

conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["postgres","since2015","192.168.3.171","jiangxi","nanchang"]

work(conp=conp)