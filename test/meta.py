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


url="http://www.dyggzy.com/categoryList_3cc01e2ead9e420db555915f5c7ae233.html"
driver=webdriver.Chrome()
# driver.minimize_window()
driver.get(url)
def general_template(tb,url,col,f3,conp):

    m=web()
    setting={
    "url":url,
    "f1":f3(a=1),
    "f2":f3(a=1),
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":1,
    'total':5


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
                time.sleep(2)

                locator=(By.XPATH,'//*[@id="center1-{}Div"]/div/a[1]/span'.format(a))
                WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

                driver.find_element_by_xpath('//*[@id="center1-{}Div"]/div/a[1]/span'.format(a)).click()
                time.sleep(2)

                locator = (By.XPATH, '//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))



            return f(*args)
        return mid
    return out

@f3
def f1(driver,num):
    locator = (By.XPATH, '//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum=driver.find_element_by_xpath("//a[@class='curret']").text

    if num!=int(cnum):

        val=driver.find_element_by_xpath('//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a').text

        driver.execute_script("_load_newsList_page('','bfbfc9ef3ed74c36b1748b5d7adbe94a','{}')".format(num))

        locator = (By.XPATH, '//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a[not(contains(string(),"%s"))]'%val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    # time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find('div', class_='tab-ul')
    tds = tables.find_all('li')
    data=[]
    for td in tds:

        href = td.a['href']
        name = td.a['title']
        ggstart_time=td.span.get_text().strip()

        tmp = [name, ggstart_time, href]
        # print(tmp)
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df

@f3()
def f2(driver):
    locator=(By.XPATH,'//*[@id="newsList"]/div/div/div[2]/div/div/div[1]/div/ul/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    total=driver.find_element_by_xpath('//*[@id="newsList"]/div/div/div[2]/div/div/div[2]/a[9]').text
    total=re.findall('共(\d+)页',total)[0]
    total=int(total)

    return total





def work(conp,i=-1):
    data=[

        #乡镇交易
        ["gggggg","http://www.dyggzy.com/categoryList_3cc01e2ead9e420db555915f5c7ae233.html",["name","ggstart_time","href"],f3],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],w[3],conp)
conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["postgres","since2015","192.168.3.171","jiangxi","fengcheng"]

work(conp=conp)