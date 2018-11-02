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
# driver.maximize_window()
driver.get('http://ggzy.haikou.gov.cn/login.do?method=newindex')
time.sleep(4)
driver.switch_to.frame('mainFrame')

driver.find_element_by_xpath("//div[@class='news news-build f_l']/h1/a").click()


locator=(By.XPATH,'/html/body/div/div[2]/div[2]/div/ul[1]/li[1]/div[1]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))


# val=driver.find_element_by_xpath("//div[@class='xxgk_navli'][1]/ul/li[3]/a").text

# driver.switch_to.parent_frame()
# time.sleep(3)
driver.execute_script('gotoPage(5)')


# locator = (By.XPATH, "//div[@class='xxgk_navli'][1]/ul/li[3]/a[not(contains(string(),'%s'))]"%val)
# WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
# #
# total=driver.find_element_by_xpath('//*[@id="page_public_info"]/a[last()]').get_attribute('paged')
# print(total)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')


time.sleep(10)


driver.quit()