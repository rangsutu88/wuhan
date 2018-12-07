
import time
from os.path import dirname, join

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
url='http://ggzy.hefei.gov.cn/gggs/003002/20181204/a0b3b622-dd61-4080-a736-7f1bdcec9c1d.html'
driver.get(url)
locator = (By.XPATH, '//div[@data-role="body"] | //div[@class="ewb-main"]')

WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


driver.switch_to.frame()
driver.switch_to.parent_frame()

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

div = soup.find('div', attrs={'data-role': "body"})
if div == None:
    div = soup.find('div', class_='ewb-main')
else:
    divs = div.find_all('div', class_="ewb-info-bd hidden")
    for d in divs:
        d.extract()
print(div)
driver.quit()