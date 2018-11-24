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
url='http://www.aqzbcg.org:1102/jyxx/012001/012001002/20181107/8d01c015-f37d-432b-9043-88624601e362.html'
driver.get(url)

locator = (By.XPATH, '/html/body')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
title = driver.title



locator = (By.CLASS_NAME, 'ewb-con')

WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

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

div = soup.find('div', class_='tab-view').find('div', attrs={'data-role': "body"})
print(div)



