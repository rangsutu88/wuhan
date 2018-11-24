import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from lxml import get_include
import lxml
import sys
import time

import json
# from zhulong.util.etl import gg_meta,gg_html

import sys
# sys.setrecursionlimit(2000)



driver=webdriver.Chrome()
url='http://ggzy.hefei.gov.cn/gggs/003002/20120924/e2b51d3f-88d7-44de-9192-0a7f4b315121.html'
# url='http://ggzy.hefei.gov.cn/gggs/003002/20130531/574e9024-6939-475a-bca6-fe6cab314b1f.html'
# url='http://ggzy.hefei.gov.cn/jyxx/002002/002002001/20181122/4a64fb6e-fe09-4389-bbdd-226b20623448.html?ztbtab=002002001'


driver.get(url)

locator = (By.XPATH, '//div[@class="ewb-main"]')

WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

before = len(driver.page_source)
time.sleep(0.1)
after = len(driver.page_source)
i = 0
while before != after:
    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i += 1
    if i > 5: break

page = driver.page_source

soup = BeautifulSoup(page, 'lxml')

div = soup.find('div', class_='ewb-info-bd').find('div',class_='ewb-info-main clearfix')
if div==None:
    div=soup.find('div',class_="ewb-info-bd")


print(div)