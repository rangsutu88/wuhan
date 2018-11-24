import time

import pandas as pd
import re

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

URL='https://exmail.qq.com/cgi-bin/frame_html?sid=E5689B1GQ6hbgxhD,7&r=907aac098371dc02ac865ef22ffe533c'
UA='stand@cardboarddisplays.com.hk'
PW='Storedisplay1234'
dirver=webdriver.Chrome()
dirver.get(URL)


def login(driver,username,password):

    driver.find_element_by_name(name='inputuin').clear()
    driver.find_element_by_name(name='inputuin').send_keys(username)
    time.sleep(2)
    driver.find_element_by_id('pp').clear()
    driver.find_element_by_id('pp').send_keys(password)
    time.sleep(2)
    driver.find_element_by_id('btlogin').click()
    time.sleep(3)
    driver.switch_to.frame('mainFrame')
    driver.find_element_by_xpath('//*[@id="TodayInBox"]/li[3]/div/a').click()
    locator=(By.XPATH,'//table[@class="i M"][1]/tbody/tr/td[last()]/table/tbody/tr/td[@class="gt tf"]/div/u')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))