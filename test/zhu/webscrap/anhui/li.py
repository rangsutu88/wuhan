import re
import time

# from selenium import webdriver
from lxml import etree
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
driver.get('http://ggzy.sqzwfw.gov.cn/jyxx/tradeInfo.html?catenum=001002')


locator = (By.CLASS_NAME, "ewb-trade-tb")
WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
locator = (By.CLASS_NAME, 'pg_maxpagenum')
WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
# print("_____")
val = driver.find_element_by_xpath("//tbody[@id='showList']/tr[1]//a").text
print(val)
cnum = int(driver.find_element_by_class_name("pg_maxpagenum").text.split('/')[0])
num=3
if cnum != num:
    time.sleep(1)
    driver.find_element_by_class_name('pg_num_input').clear()
    driver.find_element_by_class_name('pg_num_input').send_keys(num)
    driver.find_element_by_class_name("pg_gobtn").click()
    locator = (By.CLASS_NAME, "ewb-trade-tb")
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
    locator = (By.CLASS_NAME, 'pg_maxpagenum')
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
    locator = (By.XPATH, "//tbody[@id='showList']/tr[1]//a[not(contains(string(),'%s'))]" % val)
    # WebDriverWait(driver, 20).until(EC.visibility_of_element_located(locator))
    print("[INFO]已经跳转到第<{}>页".format(num))

# locator = (By.ID, 'showList')
# WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
# page = driver.page_source
# body = etree.HTML(page)
# content_list = body.xpath("//tbody[@id='showList']/tr")
# for content in content_list:
#     name = content.xpath('./td/a')[0].text
#     print(name)



page = driver.page_source
body = etree.HTML(page)

trs=body.xpath('//tr[@class="ewb-trade-tr"]')
for tr in trs:
    content=tr.xpath('./td[2]/a/@href')
    print(content)


