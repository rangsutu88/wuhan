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
url='http://www.xyggzy.cn/ggzy/InfoDetail/Default.aspx?InfoID=f05b6f87-e9ff-4e71-9dd8-722031ac7a3c&CategoryNum=016002'
driver.get(url)

locator = (By.XPATH, '//')

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
div = soup.find('td',id='Zoom2')
print(div)



