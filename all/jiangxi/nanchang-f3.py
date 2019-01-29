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


driver=webdriver.Chrome()
url='http://ncztb.nc.gov.cn/nczbw/InfoDetail/Default.aspx?InfoID=7d8899ae-4b57-48fe-8a6e-8f193ac955e0&CategoryNum=002002002'

driver.get(url)
try:
    locator = (By.XPATH, '//table[@id="tblInfo"]')
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
except:
    locator = (By.XPATH, '/html/body')
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
div = soup.find('td',id="TDContent")
if div ==None:
    div=soup.find('embed',id="plugin")
    if div == None:
        raise  ValueError

print(div)