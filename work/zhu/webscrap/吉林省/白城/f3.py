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
from lxml import etree
from lxml import get_include
import lxml
import sys
import time

import json
# from zhulong.util.etl import gg_meta,gg_html

import sys
# sys.setrecursionlimit(2000)



driver=webdriver.Chrome()
url='http://www.bcggzy.gov.cn/jyxx/003002/003002003/003002003004/20181116/29fc4ea8-7e84-460c-a3e0-5cd40df94c08.html'


driver.get(url)

locator = (By.XPATH, '//div[@class="ewb-about-content"] | //div[@class="ewb-process tabview"] | //div[@class="ewb-container ewb-alter"]')

WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
try:
    mark=driver.find_element_by_xpath('//div[@class="ewb-location"]/a[4]').text
    driver.find_element_by_xpath('//ul[@data-role="head"]/li[string()="{}"]'.format(mark)).click()
    time.sleep(0.1)
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

    div = soup.find('div', attrs={'data-role': 'tab-content', 'class': ''})

except:

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


    div = soup.find('div',class_='news-article')


print(div)