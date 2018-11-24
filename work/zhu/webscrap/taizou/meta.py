import time

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json


driver=webdriver.Chrome()
driver.maximize_window()
driver.get('http://58.222.225.18/ggzy/jyxx/004001/004001002/')



locator = (By.XPATH, "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr/td[3]/table/tbody/tr[2]/td/iframe")
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
driver.switch_to_frame(1)

locator=(By.XPATH,'nihao')
aa=EC.title_is(locator)

print('============================',aa,'===========================================')



locator = (By.XPATH, "(//div[@id='infolist']/table/tbody/tr)[last()]/td/a")
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
cnum = int(driver.find_element_by_xpath("//*[@id='MoreInfoList1_Pager']/table/tbody/tr/td[1]/font[3]/b").text[0])
# print(cnum)
# for num in range(1,10):
for num in range(1,3):
    if cnum != num:
        driver.execute_script("__doPostBack('MoreInfoList1$Pager','%d')" % num)
        # time.sleep(1)
        locator = (By.XPATH, "//*[@id='MoreInfoList1_Pager']/table/tbody/tr/td[1]/font[3]/b[string()='%s']"%num)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        print('正在爬取第{}页'.format(num))
        print(driver)


driver.quit()