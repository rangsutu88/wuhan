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
url='http://www.tlzbcg.com/tlsggzy/infodetail/?infoid=eaeb5434-aaef-442a-ac96-b0e4e770f0fa&categoryNum=006003'
driver.get(url)
locator = (By.XPATH, '//*[@id="tblInfo"] | //div[@id="menutab_6_1"]/.. | //div[@class="container clearfix"]')#枞阳县、义安区


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


# div = soup.find('td', class_="infodetail") #枞阳县、义安区

# div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})

div=soup.find('div',class_="container clearfix").find('table').find_all('tr')[2]



print(div)
driver.quit()