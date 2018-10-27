import os
import pymongo
import time
import re
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymysql import connect

URL='https://mail.qq.com/'
UA='1371214116'
PW='xinjiu522590.'

def login(driver,username,password):
    driver.switch_to.frame('login_frame')
    driver.find_element_by_name(name='u').clear()
    driver.find_element_by_name(name='u').send_keys(username)
    time.sleep(2)
    driver.find_element_by_name(name='p').clear()
    driver.find_element_by_name(name='p').send_keys(password)
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="low_login"]/a').click()
    time.sleep(1)
    driver.find_element_by_id('login_button').click()
    # time.sleep(30)
    driver.switch_to.default_content()
    time.sleep(10)
    # driver.switch_to.frame('mainFrame')
    # locator = (By.XPATH, "//div[@class='bold unread_folderlist']/a[1]")
    # WebDriverWait(driver, 40).until(EC.presence_of_element_located(locator))

def get_content(driver):
    driver.switch_to.frame('mainFrame')
    driver.find_element_by_xpath("//div[@class='bold unread_folderlist']/a[1]").click()
    driver.find_element_by_xpath("//div[@id='div_showtoday']/table[1]/tbody/tr/td[3]").click()
    HTML = driver.page_source
    soup = BeautifulSoup(HTML, 'lxml')
    conent = soup.find('div', class_='readmailinfo')
    tables = conent.find_all('table', limit=3)
    title = tables[0].find('span').get_text()
    send_bys = tables[1].find_all('span')
    send_by = send_bys[1].get_text()
    lasts = tables[2].find_all('tr', limit=2)
    send_time = lasts[0].b.get_text()
    send_to = lasts[1].get_text()
    send_to = send_to.lstrip('收件人：').strip()
    send_by_email = re.findall(r'<(.+)>', send_by)[0]


    print(title)
    print(send_by)
    print(send_time)
    print(send_to)
    print(send_by_email)

def change_page(driver):
    driver.find_element_by_xpath('//div[@id="nextmail_bt"]/a[2]').click()

def start():
    driver = webdriver.Chrome()
    time.sleep(1)
    driver.get(url=URL)
    login(driver, UA, PW)
    get_content(driver)
    change_page(driver)

    time.sleep(10)
    driver.close()
    driver.quit()

if __name__ == '__main__':

    start()

