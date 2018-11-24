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
driver.get('http://jyzx.fy.gov.cn/FuYang/jsgc/012006/012006001/')

#第一个等待
locator=(By.XPATH,'//*[@id="right"]/div[2]/div[1]/div/ul/li[1]/div/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
#点回汇总页
driver.find_element_by_xpath('//*[@id="right"]/div[1]/div/a[3]').click()

locator = (By.XPATH, '//*[@id="right"]/div[2]/div/ul[1]/li[1]/div/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


#获取总页数
html=driver.page_source
soup=BeautifulSoup(html,'lxml')
'//a[@class="block-more"]'
all_more=soup.find_all('a',class_='block-more')
all_more=int(len(all_more))

total = 0
for i in range(1,all_more+1):

    driver.find_element_by_xpath(
        '(//a[@class="block-more"])[{}]'.format(i)).click()
    locator = (By.XPATH, '//*[@id="right"]/div[2]/div[1]/div/ul/li[1]/div/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    try:
        page = driver.find_element_by_xpath('//td[@class="huifont"]').text
        total_ = re.findall(r'/(\d+)', page)[0]
    except:
        total_=0
    print(total_)
    driver.find_element_by_xpath('//*[@id="right"]/div[1]/div/a[3]').click()
    locator = (By.XPATH, '//*[@id="right"]/div[2]/div/ul[1]/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    total = total + int(total_)



print(total)


driver.quit()

