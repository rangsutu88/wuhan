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
url='http://www.laztb.gov.cn/laztb/infodetail/?infoid=24b1a820-fad8-4b8e-8957-957ba7b9a74e&categoryNum=002005001001'
driver.get(url)

'//div[@class="ewb-detail-info"]'

locator = (By.XPATH, '//div[@data-role="tab-content" and not(@class)]/div/table | //div[@class="ewb-detail-info"]')

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
try:
    div = soup.find('div',attrs={'data-role':"tab-content",'class':''})
    table=div.find('table')
    div=table.find('td',class_='infodetail')
except:
    div=soup.find('div',class_="ewb-detail-info")


print(div)
driver.quit()