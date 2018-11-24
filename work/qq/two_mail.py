import time

import pandas as pd
import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from etl.etl import gg_meta

COOKIES=[]
URL='https://exmail.qq.com/login'
UA='stand@cardboarddisplays.com.hk'
PW='Storedisplay1234'

def f1(driver,num):
    driver.maximize_window()
    url=driver.current_url
    driver.delete_all_cookies()

    for cookie in COOKIES:
        driver.add_cookie(cookie)

    time.sleep(0.5)
    driver.get('https://exmail.qq.com/cgi-bin/frame_html?sid=hQh4EvtRHvUB0EsQ,2&r=a0875d28017cee1f38f6fd2632145cc4')

    driver.switch_to.frame('mainFrame')
    driver.find_element_by_xpath('//*[@id="TodayInBox"]/li[3]/div/a').click()


    locator = (By.XPATH, '(//table[@class="i M"])[1]/tbody/tr/td[last()]/table/tbody/tr/td[@class="gt tf"]/div/u')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page = driver.find_element_by_xpath(
        '//div[@class="toolbg toolbgline toolheight nowrap"][1]/div[@class="right"]').text
    cnum = re.findall('(\d+)/', page)[0]
    cnum=int(cnum)
    num = 224
    if int(cnum) != num:

        val = driver.find_element_by_xpath(
            '(//table[@class="i M"])[1]/tbody/tr/td[last()]/table/tbody/tr/td[@class="gt tf"]/div/u').text

        driver.find_element_by_xpath(
            '//div[@class="toolbg toolbgline toolheight nowrap"][1]/div[@class="right"]/a[2]').click()
        locator = (By.XPATH, '//div[@class="addrtitle jumpmenusdjust"]/input')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        input_num = driver.find_element_by_xpath('//div[@class="addrtitle jumpmenusdjust"]/input')
        input_num.click()
        input_num.clear()
        input_num.send_keys(num)
        driver.find_element_by_xpath('//div[@class="addrtitle jumpmenusdjust"]/../a').click()
        locator = (By.XPATH, '(//table[@class="i M"])[1]/tbody/tr/td[last()]/table/tbody/tr/td[@class="gt tf"]/div/u')
        WebDriverWait(driver, 10).until_not(EC.text_to_be_present_in_element(locator, val))

    data=[]
    HTML = driver.page_source
    soup = BeautifulSoup(HTML, 'lxml')
    divs = soup.find_all('table', attrs={'class': re.compile('i M|F')})
    count=int(len(divs))
    for i in range(1,count):
        div=divs[i]
        td = div.find('tbody', recursive=False).find('tr', recursive=False).find_all('td', recursive=False)[-1]
        href = td['onclick']
        try:
            driver.execute_script(href)
        except:
            try:
                driver.switch_to.frame('mainFrame')
            except:
                pass
            try:
                driver.find_element_by_xpath('(//div[@class="nowrap qm_left"])[1]/a[1]').click()
            except:
                pass

            continue

        time.sleep(0.5)
        tmp=parse_html(driver)
        time.sleep(0.5)
        driver.back()

        data.append(tmp)
    print('doing-{}'.format(num))

    df = pd.DataFrame(data=data)

    return df


def parse_html(driver):
    try:
        driver.switch_to.frame('mainFrame')
    except:
        pass
    try:
        try:
            locator = (By.XPATH, '//div[@class="readmailinfo"]/table[1]/tbody/tr/td[1]/div[1]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            locator = (By.XPATH, '//div[@class="readmailinfo"]/table[1]/tbody/tr/td[1]/div[1]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        pass

    HTML = driver.page_source
    soup = BeautifulSoup(HTML, 'lxml')
    try:
        conent = soup.find('div', class_='readmailinfo')
        tables = conent.find_all('table', limit=3, recursive=False)
    except:
        return
    try:
        title = tables[0].find('span', id="subject").get_text()
    except:
        title = None
    try:
        send_bys = tables[1].find_all('span')

        send_by = send_bys[1].get_text()

        lasts = tables[2].find_all('tr', limit=2)
        send_time = lasts[0].b.get_text()
        send_to = lasts[1].get_text()
        send_to = send_to.lstrip('收件人：').strip()
        send_by_email = re.findall(r'<(.+)>', send_by)[0]

        tmp = [title,send_by,send_by_email,send_time, send_to]
        # print(tmp)
        return tmp

    except:

        return None



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
    locator=(By.XPATH,'(//table[@class="i M"])[1]/tbody/tr/td[last()]/table/tbody/tr/td[@class="gt tf"]/div/u')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))



def f2(driver):
    global COOKIES
    COOKIES = []
    time.sleep(2)
    login(driver,UA,PW)
    COOKIES = driver.get_cookies()
    # print(COOKIES)
    page=driver.find_element_by_xpath('//div[@class="toolbg toolbgline toolheight nowrap"][1]/div[@class="right"]').text
    total = re.findall('/(\d+)', page)[0]
    total = int(total)
    total=1
    driver.quit()
    return total


data=[

    ["mail_223","https://exmail.qq.com/cgi-bin/frame_html?sid=hQh4EvtRHvUB0EsQ,2&r=a0875d28017cee1f38f6fd2632145cc4",
     ['title','send_by','send_by_email','send_time', 'send_to'],f1,f2],

]



def work(conp):
    gg_meta(conp,data=data,diqu="彭",headless=True)



work(conp=["testor","zhulong","192.168.3.171","test","lch"])