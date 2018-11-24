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

URL='https://exmail.qq.com/cgi-bin/frame_html?sid=E5689B1GQ6hbgxhD,7&r=907aac098371dc02ac865ef22ffe533c'
UA='stand@cardboarddisplays.com.hk'
PW='Storedisplay1234'
COOKIES={}

def login(driver,username,password):
    global COOKIES

    driver.find_element_by_name(name='inputuin').clear()
    driver.find_element_by_name(name='inputuin').send_keys(username)
    time.sleep(2)
    driver.find_element_by_id('pp').clear()
    driver.find_element_by_id('pp').send_keys(password)
    time.sleep(2)
    driver.find_element_by_id('btlogin').click()
    time.sleep(2)
    COOKIES=driver.get_cookies()
    print(COOKIES)

def get_content(driver):
    driver.switch_to.frame('mainFrame')
    driver.find_element_by_xpath('//*[@id="TodayInBox"]/li[3]/div/a').click()

    locator = (By.XPATH, '//table[@class="i M"][1]/tbody/tr/td[last()]/table/tbody/tr/td[@class="gt tf"]/div/u')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page=driver.find_element_by_xpath('//div[@class="toolbg toolbgline toolheight nowrap"][1]/div[@class="right"]').text
    print(page)
    cnum=re.findall('(\d+)/',page)[0]
    total=re.findall('/(\d+)',page)[0]
    total=int(total)
    print(cnum)
    print(total)
    return total


def parse_html(driver):
    locator=(By.XPATH,'//*[@id="subject"]')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    HTML = driver.page_source
    soup = BeautifulSoup(HTML, 'lxml')
    conent = soup.find('div', class_='readmailinfo')
    tables = conent.find_all('table', limit=3,recursive=False)
    try:
        title = tables[0].find('span',id="subject").get_text()
    except:
        title=None
    try:
        send_bys = tables[1].find_all('span')

        send_by = send_bys[1].get_text()

        lasts = tables[2].find_all('tr', limit=2)
        send_time = lasts[0].b.get_text()
        send_to = lasts[1].get_text()
        send_to = send_to.lstrip('收件人：').strip()
        send_by_email = re.findall(r'<(.+)>', send_by)[0]
        time.sleep(0.1)

        time.sleep(0.1)
    except:
        url=driver.current_url
        url=url + '\n'
        print('出错了{}'.format(url))
        with open('未爬取到的链接.txt','a+',encoding='utf8') as f:
            f.write(url)


def change_page(driver):

    val=driver.find_element_by_xpath('//table[@class="i M"][1]/tbody/tr/td[last()]/table/tbody/tr/td[@class="gt tf"]/div/u').text

    driver.find_element_by_xpath('//div[@class="toolbg toolbgline toolheight nowrap"][1]/div[@class="right"]/a[2]').click()
    locator=(By.XPATH,'//div[@class="addrtitle jumpmenusdjust"]/input')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    input_num=driver.find_element_by_xpath('//div[@class="addrtitle jumpmenusdjust"]/input')
    input_num.click()
    input_num.clear()
    input_num.send_keys(3)
    driver.find_element_by_xpath('//div[@class="addrtitle jumpmenusdjust"]/../a').click()
    locator = (By.XPATH, '//table[@class="i M"][1]/tbody/tr/td[last()]/table/tbody/tr/td[@class="gt tf"]/div/u')
    WebDriverWait(driver,10).until_not(EC.text_to_be_present_in_element(locator,val))

    page = driver.find_element_by_xpath(
        '//div[@class="toolbg toolbgline toolheight nowrap"][1]/div[@class="right"]').text
    print(page)

def start():

    driver = webdriver.Chrome()
    driver.maximize_window()
    time.sleep(1)
    driver.implicitly_wait(5)
    driver.get(url=URL)
    locator=(By.XPATH,'//div[@class="login_panel"]')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    login(driver, UA, PW)
    get_content(driver)

    pagesource=driver.page_source
    print(pagesource.encode(encoding='GB18030'))

    driver.close()
    driver.quit()

    # time.sleep(4)

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)

    driver.delete_all_cookies()
    for cookie in COOKIES:
        driver.add_cookie(cookie)

    time.sleep(2)
    driver.get(URL)


    time.sleep(2)
    c=driver.get_cookies()
    print(c)
    time.sleep(10)
    driver.quit()




if __name__ == '__main__':

    start()

