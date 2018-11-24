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
driver.get('http://www.gasggzy.com/gasggzy/gcjs/009001/009001001/MoreInfo.aspx?CategoryNum=009001001')
# locator=(By.XPATH,'//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
# WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

locator=(By.XPATH,'//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
page_all=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_myGV_ctl23_LabelPageCount"]').text
print(page_all)

# driver.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$myGV$ctl23$LinkButtonNextPage','')")
# time.sleep(4)
# page_all=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_myGV_ctl23_LabelPageCount"]').text
# print(page_all)
# time.sleep(4)

driver.quit()