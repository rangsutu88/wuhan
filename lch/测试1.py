import datetime
import json
import time

import pandas as pd

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


url="http://www.hngp.gov.cn/henan/content?infoId=1547527754314617&channelCode=H601402&bz=2"
driver=webdriver.Chrome()
driver.minimize_window()
driver.get(url)



locator = (By.XPATH, '//div[@id="content"]')

WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

locator = (By.XPATH, '//div[@id="content"][string-length()>2] | //div[@id="content"][count(*)>=1]')
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
# mark=re.findall('<div class="List1 Top5">',page)


soup = BeautifulSoup(page, 'html.parser')
div = soup.find('div', id="content")
div2 = soup.find('div', class_="List1 Top5")
if div2:
    div=str(div)+str(div2)
    div = BeautifulSoup(div, 'html.parser')

print(div)
# print(div2)
# print(type(div))
# print(div)


