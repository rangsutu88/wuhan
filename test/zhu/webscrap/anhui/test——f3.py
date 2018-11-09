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

import sys
import time

import json
# from zhulong.util.etl import gg_meta,gg_html

driver=webdriver.Chrome()
url='http://ggzyjy.xuancheng.gov.cn/XCTPFront/ztbdetail/ztbjsdetail.aspx?type=1&InfoID=1ad28c78-597f-4962-85e1-cbdf3c29439a&CategoryNum=011001001'
driver.get(url)


locator = (By.XPATH, '//*[@id="form1"]/div[4]/table/tbody/tr/td/table')

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
div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})




print(div)
driver.quit()