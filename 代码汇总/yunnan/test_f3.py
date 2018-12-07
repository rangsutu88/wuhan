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

driver=webdriver.Chrome()
url='http://www.xzzbtb.gov.cn/xz/publish-notice!view.do?searchType=TENDER&SID=4028818a567d59a8015682fc08f71768'
driver.get(url)
try:
    mark=0
    driver.switch_to.frame('main')
except:
    mark=1
    pass
try:
    locator = (By.XPATH, '//div[@id="myPrintArea"] | //div[@class="x-main-news-content"]')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
except:
    if mark==0:
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
driver.switch_to.parent_frame()

soup = BeautifulSoup(page, 'lxml')
div = soup.find('div', id="myPrintArea")
if div==None:
    div=soup.find('div', class_="x-main-news-content")
    if div == None:
        div = soup.find('body')
print(div)

