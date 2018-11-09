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
url='http://www.hfggzy.com/chzbtb/infodetail/?infoid=4968e540-12c7-4c98-930d-ff641a1b86f4&categoryNum=003001004'

driver.get(url)

locator=(By.XPATH,'//div[@class="container"]/div/div[2]/table')

WebDriverWait(driver,10).until(EC.presence_of_all_elements_located(locator))

before=len(driver.page_source)
time.sleep(0.1)
after=len(driver.page_source)
i=0
while before!=after:
    before=len(driver.page_source)
    time.sleep(0.1)
    after=len(driver.page_source)
    i+=1
    if i>5:break

page=driver.page_source

soup=BeautifulSoup(page,'lxml')

div=soup.find('div',class_='container')
div_1=div.find('div')
div_2=div_1.find_all('div')[1]
table=div_2.find('table')

print(table)