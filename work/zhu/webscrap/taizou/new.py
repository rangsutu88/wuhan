import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

from lmfscrap import web


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


def f1(driver, num):
    print(driver)

    cnum = int(driver.find_element_by_xpath("//*[@id='MoreInfoList1_Pager']/table/tbody/tr/td[1]/font[3]/b").text[0])
    # print(cnum)

    if cnum != num:
        driver.execute_script("__doPostBack('MoreInfoList1$Pager','%d')" % num)
        # time.sleep(1)
        locator = (By.XPATH, "//*[@id='MoreInfoList1_Pager']/table/tbody/tr/td[1]/font[3]/b[string()='%s']" % num)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    print('正在爬第%s页'%num)
    data=[]
    df=pd.DataFrame(data=data)
    return df




def f2(driver):

    return 5

def zhongbiao_gg(f):
    def wrap(*krg):
        driver = krg[0]


        if '记录总数' not in driver.page_source:

            locator = (By.XPATH,
                "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr/td[3]/table/tbody/tr[2]/td/iframe")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            driver.switch_to_frame(1)
            locator = (By.XPATH, "(//div[@id='infolist']/table/tbody/tr)[last()]/td/a")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        else:
            print('这里这里=======================================')
        return f(*krg)
    return wrap




def general_template(tb, url, col,f, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f(f1),
        "f2": f(f2),
        "tb": tb,
        "col": col,
        "conp": conp,
        "num": 1,
        'total':5

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["gcjs_fangwushizheng_zhaobiao_gg",
         "http://58.222.225.18/ggzy/jyxx/004001/004001001/",
         ["name"],zhongbiao_gg],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2],w[3], conp)
conp=["testor","zhulong","192.168.3.171","test","public"]


work(conp=conp,i=0)