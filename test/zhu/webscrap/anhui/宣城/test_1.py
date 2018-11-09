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
driver.get('http://ggzyjy.xuancheng.gov.cn/XCTPFront/jsgc/011001/011001001/')

#第一个等待
locator=(By.XPATH,'//tr[@class="trfont"][1]/td[2]/a')

WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url
c_type=driver.find_element_by_xpath('//div[@class="ewb-now"]/span').text.strip()
c_text=driver.find_element_by_xpath('//div[@class="l ewb-fwzn"][2]/a').text.strip()
print(c_text,c_type)

print(url)
#获取总页数
PAGE=[]
#
total = 0
for i in range(1,9):

    if i != 1:
        driver.find_element_by_xpath('//div[@class="l ewb-fwzn"][1]/a').click()
        locator=(By.XPATH,'//*[@id="categorypagingcontent"]/div/div[1]/div/ul/li[1]/a')
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath('//li[@class="ewb-menu-item"][{i}]/ul/li/a[contains(string(),"{c_type}")]'.format(i=i,c_type=c_type)).click()
        locator = (By.XPATH, '//tr[@class="trfont"][1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//td[@class="huifont"]').text
        total_ = re.findall(r'/(\d+)', page)[0]
    except:
        total_=0

    print(total_)
    PAGE.append(total_)
    total = total + int(total_)


print(total)


driver.quit()

