
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
url='http://ggj.chizhou.gov.cn/chiztpfront/infodetail/?infoid=7312f500-ebbc-475a-ab43-73dc30dd3927&categoryNum=002001005001'
driver.get(url)


locator = (By.XPATH, '//*[@id="form1"]/div[4]/div/div[2]/div/table/tbody/tr/td/table | //div[@class="ewb-tell-bd"]/table')

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

    div = soup.find('div', class_="ewb-tell-bd").find_all('tr')[2]
except:
    div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})


print(div)