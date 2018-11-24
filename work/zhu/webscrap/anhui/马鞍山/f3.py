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


driver=webdriver.Chrome()

url='http://zbcg.mas.gov.cn/maszbw/ztbdetail/ztbjsdetail.aspx?type=1&InfoID=640646e9-4c30-4b34-b32f-fd468ba3743e&CategoryNum=028001001001'
driver.get(url)

locator = (By.XPATH, '//*[@id="tblInfo"] | //*[@id="form1"]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table')


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

div = soup.find('td', id="TDContent")
if div == None:
    div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})
print(div)