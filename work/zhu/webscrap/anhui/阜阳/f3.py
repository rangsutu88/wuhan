import re
import time

# from selenium import webdriver
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
url='http://jyzx.fy.gov.cn/fuyang/Error.htm?aspxerrorpath=/FuYang/ZtbInfo/ZtbDyDetail_jsgc.aspx'

def f3(driver):
    driver.get(url)

    locator = (By.XPATH, '/html/body')
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
    html = driver.page_source
    if '系统出现了错误' in html:
        return '404'
    locator = (By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/table | /html/body/div[2]/div[2]/div[2]/div')

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
    div = soup.find('div', id='mainContent')

    if div == None:
        div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})

div=f3(driver)
print(div)