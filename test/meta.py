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


from  lmfscrap import web

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://www.dyggzy.com/categoryList_3cc01e2ead9e420db555915f5c7ae233.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
def general_template(tb,url,col,mid,midd,conp):

    m=web()
    setting={
    "url":url,
    "f1":midd(f1),
    "f2":mid(f2),
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":3,
    'total':20


    }
    m=web()
    m.write(**setting)

def f3(a):
    def out(f):
        def mid(*args):
            driver=args[0]
            page_source=driver.page_source
            if '末页' not in page_source:

                locator=(By.XPATH,'//*[@id="parent_center1-{}"]/span'.format(a))
                WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
                driver.find_element_by_xpath('//*[@id="parent_center1-{}"]/span'.format(a)).click()
                # time.sleep(2)

                locator=(By.XPATH,'//*[@id="center1-{}Div"]/div/a[1]/span'.format(a))
                WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

                driver.find_element_by_xpath('//*[@id="center1-{}Div"]/div/a[1]/span'.format(a)).click()
                # time.sleep(2)

                locator = (By.XPATH, '//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))



            return f(*args)
        return mid
    return out

def f4(a,page_mark):
    def out(f):
        def mid(*args):
            driver=args[0]
            num=args[1]
            page_source=driver.page_source
            if '末页' not in page_source:

                locator=(By.XPATH,'//*[@id="parent_center1-{}"]/span'.format(a))
                WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
                driver.find_element_by_xpath('//*[@id="parent_center1-{}"]/span'.format(a)).click()
                # time.sleep(2)

                locator=(By.XPATH,'//*[@id="center1-{}Div"]/div/a[1]/span'.format(a))
                WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

                driver.find_element_by_xpath('//*[@id="center1-{}Div"]/div/a[1]/span'.format(a)).click()
                # time.sleep(2)

                locator = (By.XPATH, '//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

                locator = (By.XPATH, '//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

            cnum = driver.find_element_by_xpath("//a[@class='curret']").text

            print('---zhelizhelizheli---')

            if num != int(cnum):
                val = driver.find_element_by_xpath(
                    '//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a').text

                driver.execute_script("_load_newsList_page('','{pg}','{num}')".format(pg=page_mark,num=num))

                locator = (By.XPATH,
                           '//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a[not(contains(string(),"%s"))]' % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

            return f(*args)
        return mid
    return out

def f1(driver,num):

    # time.sleep(3)
    print('正在爬取第{}页'.format(num))
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find('div', class_='tab-ul')
    tds = tables.find_all('li')
    data = []
    for td in tds:
        href = td.a['href']
        name = td.a['title']
        ggstart_time = td.span.get_text().strip()

        tmp = [name, ggstart_time, href]
        print(tmp)
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df

# def f1(driver,num):
#     locator = (By.XPATH, '//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a')
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
#
#     cnum=driver.find_element_by_xpath("//a[@class='curret']").text
#
#     if num!=int(cnum):
#
#         val=driver.find_element_by_xpath('//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a').text
#
#         driver.execute_script("_load_newsList_page('','{}','{}')".format(num))
#
#         locator = (By.XPATH, '//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a[not(contains(string(),"%s"))]'%val)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
#
#     time.sleep(3)
#     print('正在爬取第{}页'.format(num))
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'lxml')
#     tables = soup.find('div', class_='tab-ul')
#     tds = tables.find_all('li')
#     data=[]
#     for td in tds:
#
#         href = td.a['href']
#         name = td.a['title']
#         ggstart_time=td.span.get_text().strip()
#
#         tmp = [name, ggstart_time, href]
#         print(tmp)
#         data.append(tmp)
#     df=pd.DataFrame(data=data)
#     return df


def f2(driver):
    locator=(By.XPATH,'//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    # time.sleep(3)
    total=driver.find_element_by_xpath('//*[@id="newsList"]/div/div/div[2]/div/div/div[2]/a[9]').text
    total=re.findall('共(\d+)页',total)[0]
    total=int(total)

    driver.quit()
    return total





mid_5=f3(5)

midd_5=f4(5,'cd21cd48588b42b490af41f535764940')


def work(conp,i=-1):
    data=[

        #乡镇交易
        ["gggggg","http://www.dyggzy.com/categoryList_3cc01e2ead9e420db555915f5c7ae233.html",["name","ggstart_time","href"],f3(1),f4(1,'bfbfc9ef3ed74c36b1748b5d7adbe94a')],
        ["ssssss","http://www.dyggzy.com/categoryList_3cc01e2ead9e420db555915f5c7ae233.html",["name","ggstart_time","href"],mid_5,midd_5],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],w[3],w[4],conp)
conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["postgres","since2015","192.168.3.171","jiangxi","fengcheng"]

work(conp=conp)