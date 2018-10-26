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
    # locator = (By.XPATH, '//*[@id="contentlist"]/div[1]')
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    cnum=driver.find_element_by_class_name("active").text
    val=driver.find_element_by_xpath('//*[@id="contentlist"]/div[1]/div[2]').text
    url=driver.current_url
    if int(cnum) != num:

        driver.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$Pager','%d')"%num)
        locator = (By.XPATH, '//*[@id="contentlist"]/div[1]/div[2][string()!="%s"]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find('div', id='contentlist')
    table = tables.find_all('div', recursive=False)
    data=[]

    for i in table:
        a_ = i.find('a')
        href = a_['href']
        title = a_.get_text()
        content = i.find_all('div')

        if url=='https://www.cdggzy.com/site/Notice/ZFCG/NoticeList.aspx':

            rindex = url.rfind('/')
            href = url[:rindex] + '/' + href

        address = content[0].get_text().rstrip('】').lstrip('【')
        data_time_ing = content[2].find_all('div')
        data_time = data_time_ing[0].get_text()
        ing = data_time_ing[1].get_text()
        tmp=[address,title,href,ing,data_time]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    print('完成{}页'.format(num))
    return df




def f2(driver):
    time.sleep(4)
    locator=(By.XPATH,'//*[@id="contentlist"]/div[1]')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    total = driver.find_element_by_xpath('//*[@id="LabelPage"]').text.split('/')[1]
    total=int(total)
    driver.quit()
    return total

def zhaobiao_gg(f):
    def wrap(*krg):
        driver=krg[0]
        time.sleep(0.5)
        locator = (By.XPATH, '//*[@id="contentlist"]/div[1]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        text = driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[2]').get_attribute('class')
        print(text)
        print(text !='option choosed')
        print(text =='option choosed')

        if text != 'option choosed':
            locator = (By.ID, "linkbtnSrc")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            val = driver.find_element_by_xpath('//*[@id="linkbtnSrc"]').text
            driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[2]').click()
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

def biangeng_gg(f):
    def wrap(*krg):
        driver=krg[0]
        time.sleep(0.5)
        locator = (By.XPATH, '//*[@id="contentlist"]/div[1]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        text = driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[3]').get_attribute('class')
        print(text)
        print(text !='option choosed')
        print(text =='option choosed')

        if text != 'option choosed':
            locator = (By.ID, "linkbtnSrc")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

            val = driver.find_element_by_xpath('//*[@id="linkbtnSrc"]').text
            driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[3]').click()

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
def pingbiaojieguo_gg(f):
    def wrap(*krg):
        driver=krg[0]
        time.sleep(0.5)
        locator = (By.XPATH, '//*[@id="contentlist"]/div[1]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        text = driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[5]').get_attribute('class')
        print(text)
        print(text !='option choosed')
        print(text =='option choosed')

        if text != 'option choosed':
            locator = (By.ID, "linkbtnSrc")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            val = driver.find_element_by_xpath('//*[@id="linkbtnSrc"]').text
            driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[5]').click()

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
def qianyuelvxing_gg(f):
    def wrap(*krg):
        driver=krg[0]
        time.sleep(0.5)
        locator = (By.XPATH, '//*[@id="contentlist"]/div[1]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        text = driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[6]').get_attribute('class')
        print(text)
        print(text !='option choosed')
        print(text =='option choosed')

        if text != 'option choosed':
            locator = (By.ID, "linkbtnSrc")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[6]').click()
            val = driver.find_element_by_xpath('//*[@id="linkbtnSrc"]').text
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

def liubiao_gg(f):
    def wrap(*krg):
        driver=krg[0]
        time.sleep(0.5)
        locator = (By.XPATH, '//*[@id="contentlist"]/div[1]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        text = driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[7]').get_attribute('class')
        print(text)
        print(text !='option choosed')
        print(text =='option choosed')

        if text != 'option choosed':
            locator = (By.ID, "linkbtnSrc")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[7]').click()
            val = driver.find_element_by_xpath('//*[@id="linkbtnSrc"]').text
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


def general_template(tb,url,col,f,conp):

    m=web()
    setting={
    "url":url,
    "f1":f(f1),
    "f2":f(f2),
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":10,



    }
    m=web()
    m.write(**setting)

def work(conp,i=-1):
    data=[
    ["zfcg_zhaobiao_gg","https://www.cdggzy.com/site/Notice/ZFCG/NoticeList.aspx",['address','title','href','status','data_time'],zhaobiao_gg],
    ["zfcg_biangeng_gg","https://www.cdggzy.com/site/Notice/ZFCG/NoticeList.aspx",['address','title','href','status','data_time'],biangeng_gg],
    ["zfcg_zhongbiao_gg","https://www.cdggzy.com/site/Notice/ZFCG/NoticeList.aspx",['address','title','href','status','data_time'],zhongbiao_gg],
    ["gcjs_zhongbiao_gg","https://www.cdggzy.com/site/JSGC/List.aspx",['address','title','href','status','data_time'],zhaobiao_gg],
    ["gcjs_zhongbiao_gg","https://www.cdggzy.com/site/JSGC/List.aspx",['address','title','href','status','data_time'],zhongbiao_gg],
    ["gcjs_zhongbiao_gg","https://www.cdggzy.com/site/JSGC/List.aspx",['address','title','href','status','data_time'],biangeng_gg],
    ["gcjs_zhongbiao_gg","https://www.cdggzy.com/site/JSGC/List.aspx",['address','title','href','status','data_time'],pingbiaojieguo_gg],
    ["gcjs_zhongbiao_gg","https://www.cdggzy.com/site/JSGC/List.aspx",['address','title','href','status','data_time'],qianyuelvxing_gg],
    ["gcjs_zhongbiao_gg","https://www.cdggzy.com/site/JSGC/List.aspx",['address','title','href','status','data_time'],liubiao_gg],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],w[3],conp)

# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","sichuan","chengdu"]

work(conp=conp)