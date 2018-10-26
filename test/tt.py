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

driver.get('https://www.cdggzy.com/site/JSGC/List.aspx')

locator=(By.ID,"LabelPage")
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
# driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[2]').click()
driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[]').click()
time.sleep(5)
# val=driver.find_element_by_xpath('//*[@id="LabelPage"]').text
# locator=(By.XPATH,'//*[@id="LabelPage"][string()!="%s"]'%val)
# WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
# time.sleep(4)
#
# page=driver.find_element_by_xpath('//*[@id="LabelPage"]').text.split('/')[1]
#
# print(page)

# locator=(By.XPATH,'//*[@id="contentlist"]/div[1]')
# WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

# val = driver.find_element_by_xpath('//*[@id="linkbtnSrc"]').text
# locator = (By.XPATH, '//*[@id="linkbtnSrc"][string()="%s"]' %val)

# WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
# print('ok')
# text=driver.find_element_by_xpath('//*[@id="contentlist"]/div[1]').text
# print(text)
# text=driver.find_element_by_xpath('//*[@id="condition"]/div[1]/div[2]/div[2]').get_attribute('class')
# print(text)
# print(text=='option choosed')
# url=driver.current_url
# html=driver.page_source
# soup=BeautifulSoup(html,'lxml')
# tables=soup.find('div',id='contentlist')
# table=tables.find_all('div',recursive=False)
#
# for i in table:
#     a_=i.find('a')
#     href=a_['href']
#     title=a_.get_text()
#     content=i.find_all('div')
#
#     address=content[0].get_text().rstrip('】').lstrip('【')
#     data_time_ing=content[2].find_all('div')
#     data_time=data_time_ing[0].get_text()
#     ing=data_time_ing[1].get_text()
#
#     # driver.find_element_by_class_name()
#     print(address)
#
#     print(data_time)
#     print(ing)
#     print(href)
#     print(url)
#     print(title)


    # rindex=url.rfind('/')
    # href=url[:rindex]+'/'+href
    # print(href)


driver.quit()