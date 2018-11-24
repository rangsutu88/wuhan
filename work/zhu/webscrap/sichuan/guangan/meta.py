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
    locator=(By.XPATH,'//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[2]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    cnum=driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text

    val=driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
    if int(cnum) != num:

        driver.execute_script("__doPostBack('MoreInfoList1$Pager','{}')".format(num))
        locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]'%val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', id='MoreInfoList1_DataGrid1')
    trs = table.find_all('tr')
    data=[]
    for tr in trs:
        tds = tr.find_all('td')
        href = tds[1].a['href']
        href = 'http://www.gasggzy.com' + href
        title = tds[1].a['title']
        date_time = tds[2].get_text().strip()
        tmp = [title, href,date_time]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    print('完成{}页'.format(num))
    return df




def f2(driver):
    locator = (By.XPATH, '//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    total = driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text
    total=int(total)
    driver.quit()


    return total


def zhongbiao_gg(f):
    def wrap(*krg):
        driver=krg[0]
        time.sleep(0.5)
        locator = (By.XPATH, '//*[@id="contentlist"]/div[1]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        text = driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[4]').get_attribute('class')
        print(text)
        print(text !='option choosed')
        print(text =='option choosed')

        if text != 'option choosed':
            locator = (By.ID, "linkbtnSrc")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            val = driver.find_element_by_xpath('//*[@id="linkbtnSrc"]').text
            driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[4]').click()

            locator = (By.XPATH, '//*[@id="linkbtnSrc"][not(contains(string(),"%s"))]' %val)
            # val=driver.find_element_by_xpath('//*[@id="LabelPage"]').text
            # locator=(By.XPATH, '//*[@id="LabelPage"][not(contains(string(),"%s"))]' %val)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            print('zouzhezouzhe------------------------------')
        else:
            print('hehehehehehehe==================')
            pass


        return f(*krg)
    return wrap



def general_template(tb,url,col,conp):

    m=web()
    setting={
    "url":url,
    "f1":f1,
    "f2":f2,
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":2,
        'total':10



    }
    m=web()
    m.write(**setting)

def work(conp,i=-1):
    data=[
    ["gcjs_zhaobiao_gg","http://www.gasggzy.com/gasggzy/gcjs/009001/009001001/MoreInfo.aspx?CategoryNum=009001001",['title','href','data_time']],
    ["gcjs_gengzhen_gg","http://www.gasggzy.com/gasggzy/gcjs/009001/009001002/MoreInfo.aspx?CategoryNum=009001002",['title','href','data_time']],
    ["gcjs_kaibiaojilu_gg","http://www.gasggzy.com/gasggzy/gcjs/009001/009001002/MoreInfo.aspx?CategoryNum=009001003",['title','href','data_time']],
    ["gcjs_zhongbiaohouxuanren_gg","http://www.gasggzy.com/gasggzy/gcjs/009001/009001002/MoreInfo.aspx?CategoryNum=009001004",['title','href','data_time']],
    ["gcjs_zhongbiaohouxuanrenbiangeng_gg","http://www.gasggzy.com/gasggzy/gcjs/009001/009001002/MoreInfo.aspx?CategoryNum=009001005",['title','href','data_time']],
    ["gcjs_jingzhengxingtanpan_gg","http://www.gasggzy.com/gasggzy/gcjs/009001/009001002/MoreInfo.aspx?CategoryNum=009001006",['title','href','data_time']],
    ["zfcg_zhaobiao_gg","http://www.gasggzy.com/gasggzy/gcjs/009001/009001002/MoreInfo.aspx?CategoryNum=010001002",['title','href','data_time']],
    ["zfcg_zhongbiao_gg","http://www.gasggzy.com/gasggzy/zfcg/010001/010001003/MoreInfo.aspx?CategoryNum=010001003",['title','href','data_time']],
    ["zfcg_biangeng_gg","http://www.gasggzy.com/gasggzy/zfcg/010001/010001003/MoreInfo.aspx?CategoryNum=010001004",['title','href','data_time']],
    ["zfcg_qita_gg","http://www.gasggzy.com/gasggzy/zfcg/010001/010001003/MoreInfo.aspx?CategoryNum=010001005",['title','href','data_time']],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)

conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["postgres","since2015","192.168.3.171","sichuan","chengdu"]

work(conp=conp)