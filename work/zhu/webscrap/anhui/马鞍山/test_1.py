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

url='http://zbcg.mas.gov.cn/maszbw/jygg/028007/028007001/MoreInfo.aspx?CategoryNum=028007001'
driver.get(url)

locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
c_text = driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[4]/font').text.strip()

cnum= driver.find_element_by_xpath('//div[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text
print(cnum)

print(c_text)
PAGE=[]
CC_TEXT=[]
total=0
for i in range(1,5):
    if i != 1:
        mark = driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[2]/font')
        if mark == '标前公示':
            driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[2]').click()
        else:
            driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[3]').click()
        locator = (By.XPATH, '(//font[@class="MoreinfoColor"])[{}]'.format(i))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        locator = (By.XPATH, '//tr[@class="TDStylemore"][1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_link_text('更多信息').click()
        locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        total_ = driver.find_element_by_xpath('//div[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text
    except:
        total_ = 0
    c_text = driver.find_element_by_xpath('//font[@class="currentpostionfont"]/../font[2]/a[4]/font').text.strip()
    total_=int(total_)
    PAGE.append(total_)
    CC_TEXT.append(c_text)
    total = total + int(total_)
total = int(total)
print(PAGE)
print(CC_TEXT)
print(total)

driver.quit()

