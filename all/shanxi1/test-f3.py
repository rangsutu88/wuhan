import json
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
url='http://www.sxbid.com.cn/f/view-6796f0c147374f85a50199b38ecb0af6-21930.html?loginFlag=loginAndPayAndTime'

driver.get(url)

try:
    locator=(By.XPATH,'//form[@id="loginForm"]')
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(locator))
    print('登录')

except:
    locator = (By.XPATH, '//div[@class="page_main"]')
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
div = soup.find('div', class_="page_main")
try:
    div.find('p',class_="article_info").extract()
except:
    pass

print(div)