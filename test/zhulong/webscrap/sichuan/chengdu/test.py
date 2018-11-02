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

url="https://www.cdggzy.com/site/JSGC/List.aspx"
driver=webdriver.Chrome()
# driver.minimize_window()
driver.get(url)

def zhaobiao_gg(f):
    def wrap(*krg):
        driver=krg[0]

        locator = (By.XPATH, "//div[@id='contentlist']/div[1]/div[2]/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        # text = driver.find_element_by_xpath("//div[@id='displaytype']").get_attribute('class')
        text=driver.find_element_by_xpath('//*[@id="LabelPage"]').text
        text=text.split('/')[1]
        print(text)
        if text != '1222':

            val = driver.find_element_by_xpath("//div[@id='contentlist']/div[1]/div[2]/a").text
            print(val,'--------------zhuangshiqi--------------')
            driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[2]').click()

            print('..........已经点击。。。。。。。。。')
            locator = (By.XPATH, '//div[@id="contentlist"]/div[1]/div[2]/a[not(contains(string(),"%s"))]'%val)
            print('。。。。。。。正在等待。。。。。。。。')
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        return f(*krg)
    return wrap

@zhaobiao_gg
def f1(driver,num):
    print('正在爬{}页'.format(num))

    cnum=driver.find_element_by_class_name("active").text
    val=driver.find_element_by_xpath('//*[@id="contentlist"]/div[1]/div[2]/a').text
    print('-------------f1------------------',val)
    url=driver.current_url
    if int(cnum) != num:
        # time.sleep(5)
        driver.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$Pager','%d')"%num)

        locator = (By.XPATH, '//*[@id="contentlist"]/div[1]/div[2]/a[string()!="%s"]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    # html = driver.page_source
    # soup = BeautifulSoup(html, 'lxml')
    # tables = soup.find('div', id='contentlist')
    # table = tables.find_all('div', recursive=False)
    # data=[]
    #
    # for i in table:
    #     a_ = i.find('a')
    #     href = a_['href']
    #     title = a_.get_text()
    #     content = i.find_all('div')
    #
    #     if url=='https://www.cdggzy.com/site/Notice/ZFCG/NoticeList.aspx':
    #
    #         rindex = url.rfind('/')
    #         href = url[:rindex] + '/' + href
    #
    #     address = content[0].get_text().rstrip('】').lstrip('【')
    #     data_time_ing = content[2].find_all('div')
    #     data_time = data_time_ing[0].get_text()
    #     ing = data_time_ing[1].get_text()
    #     tmp=[address,title,href,ing,data_time]
    #
    #     data.append(tmp)
    # df=pd.DataFrame(data=data)
    print('完成{}页'.format(num))

    # return df