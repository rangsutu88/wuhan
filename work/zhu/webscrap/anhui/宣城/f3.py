
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


url='http://ggzyjy.xuancheng.gov.cn/XCTPFront/ztbdetail/ztbjsdetail.aspx?type=1&InfoID=4211a67c-5d81-4ab7-8dab-75166ecd2102&CategoryNum=011003001'

driver=webdriver.Chrome()
driver.get(url)


locator = (By.XPATH, '//*[@id="form1"]/div[4]/table/tbody/tr/td/table | //div[@class="ewb-main"]')

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
# div=soup.find('div',id="mainContent")


try:
    div=soup.find('div',id="mainContent")
    if div == None:
        div=soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})
except:
    div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})

print(div)