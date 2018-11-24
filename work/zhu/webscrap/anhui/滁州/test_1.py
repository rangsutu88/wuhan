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
driver.get('http://www.czggzy.gov.cn/Front_jyzx/jyxx/002008/002008003/002008003001/')

#第一个等待
locator=(By.XPATH,'//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url

#获取总页数


total = 0
for i in range(1,10):
    if i != 1:
        val = driver.find_element_by_xpath('//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a').text
        driver.find_element_by_xpath(
            '(//td[@class="LeftMenuSubbg" and not(@style)])[last()]/table/tbody/tr[{}]/td/a'.format(i)).click()
        locator = (By.XPATH, '//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
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

