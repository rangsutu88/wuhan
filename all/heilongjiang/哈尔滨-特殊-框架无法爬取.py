import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

from lch.zhulong import est_tbs,est_meta,est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]

#
# url="http://www.hljcg.gov.cn/xwzs!queryXwxxqx.action?lbbh=52301"
# driver=webdriver.Chrome()
# driver.maximize_window()
# driver.get(url)
# # #

COOKIES = {}

_name_='haerbin'

def f1(driver, num):
    locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    while True:
        cnum = driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[last()]/td/table/tbody/tr/td/span').text.strip()
        cnum=int(cnum)
        if cnum == num:
            break
        if cnum <= num:
            if (num//10-cnum//10)>=2 or ((num//10-cnum//10)==1 and num%10!=0 ):
                val = driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a').text
                driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[last()]/td/table/tbody/tr/td[last()]').click()
                try:
                    locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
                except:
                    time.sleep(5)
            else:

                val = driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a').text

                driver.execute_script("javascript:__doPostBack('GV_Data','Page${}')".format(num))

                locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        if cnum >= num:
            if (cnum//10-num//10)>=2 or ((cnum//10-num//10)==1 and cnum%10!=0 ):
                val = driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a').text
                driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[last()]/td/table/tbody/tr/td[1]/a').click()
                try:
                    locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
                except:
                    time.sleep(5)
            else:

                val = driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a').text

                driver.execute_script("javascript:__doPostBack('GV_Data','Page${}')".format(num))

                locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('table', id='GV_Data')
    divs = div.find_all('tr', style="height:22px;")

    for li in divs:
        tds = li.find_all('td')
        href_ = tds[1].a['href']
        name = tds[1].a.get_text()
        ggstart_time = tds[2].get_text()
        click_num = tds[3].get_text()
        driver.execute_script(href_)
        WebDriverWait(driver, 10).until(lambda driver: any(i in driver.current_url for i in ['TenderContent','SuccessfulContent']))
        href = driver.current_url
        driver.back()

        tmp = [name, ggstart_time, href, click_num]

        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    while True:
        val = driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a').text
        driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[last()]/td/table/tbody/tr/td[last()]').click()
        try:
            locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(5)
        try:
            driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[last()]/td/table/tbody/tr/td[last()]/a')
        except:
            total = driver.find_element_by_xpath(
                '//*[@id="GV_Data"]/tbody/tr[last()]/td/table/tbody/tr/td[last()]').text
            break
    total = int(total)
    driver.quit()

    return total


def get_cookie(driver):
    mark=driver.current_url
    global COOKIES

    COOKIES = {}
    driver.get('http://hrbggzy.org.cn/')
    locator = (By.XPATH, '//*[@id="Map"]/area[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, '//*[@id="Map"]/area[1]')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator)).click()
    handles = driver.window_handles
    driver.close()
    driver.switch_to.window(handles[1])

    locator = (By.XPATH, '//div[@class="cen_new"]/div[2]/div/div[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    if '52301' in mark:
        driver.find_element_by_xpath('//div[@class="right_foot"]/div[1]/div[2]/div[4]/div[2]/a').click()
    else:
        driver.find_element_by_xpath('//div[@class="cen_new"]/div[2]/div/div[2]/a').click()

    locator = (By.XPATH, '//div[@class="yahoo"]/div[1]/span/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))




def f4(driver, num):
    driver.maximize_window()
    global COOKIES
    mark = driver.current_url

    if num%20==1 or ('2301' in mark):
        get_cookie(driver)

    COOKIES = driver.get_cookies()[0]
    driver.add_cookie(COOKIES)

    locator = (By.XPATH, '//div[@class="yahoo"]/div[1]/span/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    cnum = driver.find_element_by_xpath('//div[@class="yahoo2"]/div/span/b[2]').text.strip()
    cnum = re.findall('(\d+)/', cnum)[0]
    if cnum != str(num):
        val = driver.find_element_by_xpath('//div[@class="yahoo"]/div[1]/span/a').text
        driver.execute_script("javascript:jump('{}');return false;".format(num))
        try:
            locator = (By.XPATH, '//div[@class="yahoo"]/div[1]/span/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(5)
    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_='yahoo')
    divs = div.find_all('div', class_="xxei")

    for li in divs:
        href = li.find('span', class_="lbej").a['onclick']
        name = li.find('span', class_="lbej").a.get_text()
        ggstart_time = li.find('span', class_="sjej").get_text()
        address = li.find('span', class_="nrej").get_text()
        href = re.findall('javascript:location.href=(.+);return false', href)[0].strip("'")

        if 'http' in href:
            href = href
        else:
            href = 'http://www.hljcg.gov.cn' + href

        tmp = [address, name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f5(driver):
    mark = driver.current_url
    global COOKIES
    COOKIES = {}

    driver.get('http://hrbggzy.org.cn/')
    locator = (By.XPATH, '//*[@id="Map"]/area[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, '//*[@id="Map"]/area[1]')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator)).click()
    handles = driver.window_handles
    driver.close()
    driver.switch_to.window(handles[1])

    locator = (By.XPATH, '//div[@class="cen_new"]/div[2]/div/div[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    if '52301' in mark:
        driver.find_element_by_xpath('//div[@class="right_foot"]/div[1]/div[2]/div[4]/div[2]/a').click()
    else:
        driver.find_element_by_xpath('//div[@class="cen_new"]/div[2]/div/div[2]/a').click()

    locator = (By.XPATH, '//div[@class="yahoo"]/div[1]/span/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page = driver.find_element_by_xpath('//div[@class="yahoo2"]/div/span/b[2]').text
    page = re.findall('/(\d+)', page)[0]
    COOKIES = driver.get_cookies()[0]

    total = int(page)
    driver.quit()
    return total


# def f6(driver):
#     url = driver.current_url
#     if 'ZBMore' in url:
#         total = 1430
#
#     if 'KBMore' in url:
#         total = 1330
#
#     driver.quit()
#     return total


def f3(driver, url):
    driver.get(url)
    url = driver.current_url

    locator = (By.XPATH, '//div[@id="main_box"]/table/tbody/tr[4] | //div[@class="xxej"]')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')
    div = soup.find('div', id="main_box").find('table').find('tbody').find_all('tr', recursive=False)[3]
    if div == None:
        div= soup.find('div',class_="xxej")

    return div


data = [
    #包含：招标，澄清，流标
    ["gcjs_gg", "http://113.6.234.4/Bid_Front/ZBMore.aspx?t=%u5168%u90e8",
     ["name", "ggstart_time", "href", 'click_num', "info"], f1, f2],
    ["gcjs_zhongbiaohx_gg", "http://113.6.234.4/Bid_Front/KBMore.aspx?t=%u5168%u90e8",
     ["name", "ggstart_time", "href", 'click_num', "info"], f1, f2],


    ["zfcg_zhaobiao_gg","http://www.hljcg.gov.cn/xwzs!queryXwxxqx.action?lbbh=42301",
     ['address',"name","ggstart_time","href","info"],f4,f5],
    #####包含流标，中标
    ["zfcg_zhong_gg", "http://www.hljcg.gov.cn/xwzs!queryXwxxqx.action?lbbh=52301",
     ['address', "name", "ggstart_time", "href", "info"], f4, f5],
]

def work(conp,**args):
    est_meta(conp,data=data,diqu="黑龙江省哈尔滨市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':


    conp=["postgres", "since2015", "192.168.3.171", "heilongjiang", "haerbin"]
    work(conp=conp)