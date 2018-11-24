import time

import pandas as pd
import re

from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lmfscrap import web




driver=webdriver.Chrome()

url='http://www.hnsztb.cn/HNWeb_NEW/jyxx/002001/002001001/002001001001/?Paging=1'
driver.get(url)

locator = (By.XPATH, '//li[@class="ewb-info-item"][1]/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

c_text = driver.find_element_by_xpath('//div[@class="ewb-location"]/span').text.strip()

cnum= driver.find_element_by_xpath('//td[@class="huifont"]').text
cnum=re.findall('(\d+)/',cnum)[0]
print(cnum)


print(c_text)
PAGE=[]
CC_TEXT=[]
total=0

for i in range(1,4):
    if i != 1:
        driver.find_element_by_xpath('//div[@class="ewb-location"]/a[4]').click()
        locator = (By.XPATH, '//div[@class="ewb-info-hd"][{}]/a[2]'.format(i))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        locator = (By.XPATH, '//div[@class="pagemargin"]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    try:
        total_ = driver.find_element_by_xpath('//td[@class="huifont"]').text
        total_=re.findall('/(\d+)',total_)[0]
    except:
        total_ = 0
    c_text = driver.find_element_by_xpath('//div[@class="ewb-location"]/span').text.strip()

    total_=int(total_)
    PAGE.append(total_)
    CC_TEXT.append(c_text)
    total = total + int(total_)
total = int(total)
print(PAGE)
print(CC_TEXT)
print(total)

driver.quit()

