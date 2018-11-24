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


#初始化
driver=webdriver.Chrome()
driver.get('http://www.szggzyjy.cn/szfront/jyxx/002001/002001001/002001001001/')

#第一个等待
locator=(By.XPATH,'//ul[@class="ewb-lbd-items"]/li/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url

#获取总页数


total = 0
for i in range(1,7):
    if i != 1:
        val = driver.find_element_by_xpath('//ul[@class="ewb-lbd-items"]/li/a').text
        driver.find_element_by_xpath(
            '//td[@class="LeftMenuSubBg" and not(@style)]/table/tbody/tr/td[not(@style or @class)]/table/tbody/tr[{}]/td/a'.format(i)).click()
        locator = (By.XPATH, '//ul[@class="ewb-lbd-items"]/li/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    try:
        page = driver.find_element_by_xpath('//td[@class="huifont"]').text
        total_ = re.findall(r'/(\d+)', page)[0]
    except:
        total_=0
    print(total_)

    total = total + int(total_)


print(total)


driver.quit()

