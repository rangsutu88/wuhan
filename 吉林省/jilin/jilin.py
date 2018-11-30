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

from zhulong.util.etl import est_tbs,est_meta,est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]

#
# url="http://www.hljcg.gov.cn/xwzs!queryXwxxqx.action?lbbh=42301"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
# #



_name_='jilin'

def f1(driver, num):
    try:
        locator = (By.XPATH, '//ul[@id="demoContent"]/li/a')
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
    except:
        time.sleep(5)

    while True:

        cnum = driver.find_element_by_xpath('//div[@id="pages"]/span').text.strip()
        cnum = int(cnum)

        try:
            val = driver.find_element_by_xpath('//ul[@id="demoContent"]/li/a').text
        except:
            val = 'none'

        if cnum == num:
            try:
                driver.find_element_by_xpath('//ul[@id="demoContent"]/li/a')
            except:
                driver.refresh()
                time.sleep(1)
            break
        if cnum < num:
            if (num - cnum) >= 5:
                if (num - cnum) >= 20:
                    chang = (num - cnum) // 5 - 3
                    for i in range(chang):
                        driver.find_element_by_xpath('//div[@id="pages"]/a[last()-1]').click()

                driver.find_element_by_xpath('//div[@id="pages"]/a[last()-1]').click()
            else:
                driver.find_element_by_xpath('//div[@id="pages"]/a[@class="next"]').click()
            try:
                locator = (By.XPATH, '//ul[@id="demoContent"]/li/a[not(contains(string(),"%s"))]' % val)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            except:
                time.sleep(5)
        if cnum > num:
            if (cnum - num) >= 5:
                if (cnum - num) >= 20:
                    chang = (cnum - num) // 5 - 3
                    for i in range(chang):
                        driver.find_element_by_xpath('//div[@id="pages"]/a[2]').click()

                driver.find_element_by_xpath('//div[@id="pages"]/a[2]').click()
            else:
                driver.find_element_by_xpath('//div[@id="pages"]/a[@class="prev"]').click()

            try:
                locator = (By.XPATH, '//ul[@id="demoContent"]/li/a[not(contains(string(),"%s"))]' % val)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            except:
                time.sleep(5)

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('ul', id='demoContent')
    divs = div.find_all('li')

    for li in divs:
        href = li.a['href']
        name = li.a.get_text()
        address = li.find('span', class_='arealeft').get_text()
        ggstart_time = li.find('span', class_='ewb-list-date').get_text()
        if 'http' in href:
            href = href
        else:
            href = 'http://www.jl.gov.cn' + href

        tmp = [name, ggstart_time, href, address]

        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//ul[@id="demoContent"]/li/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    while True:
        try:
            val = driver.find_element_by_xpath('//ul[@id="demoContent"]/li/a').text
        except:
            val = 'none'

        driver.find_element_by_xpath('//div[@id="pages"]/a[last()-1]').click()
        try:
            locator = (By.XPATH, '//ul[@id="demoContent"]/li/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(5)

        text = driver.find_element_by_xpath('//div[@id="pages"]/a[last()]').text
        if text != '下一页>':
            page = driver.find_element_by_xpath('//div[@id="pages"]/span').text.strip()
            break

    total = int(page)
    driver.quit()

    return total

#
# def f4(driver):
#     url = driver.current_url
#     if 'cggg' in url:
#         total = 2498
#     if 'bggg' in url:
#         total = 467
#     if 'zbgg' in url:
#         total = 1506
#     driver.quit()
#     return total


def f3(driver, url):
    driver.get(url)
    url = driver.current_url

    locator = (By.XPATH, '//div[@class="ewb-article"]')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

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
    div = soup.find('div', class_="ewb-article-info")

    return div


data = [
    ["gcjs_zhaobiao_gg","http://www.jl.gov.cn/ggzy/gcjs/zbgg/",["name","ggstart_time","href",'address',"info"],f1,f2],
    ["gcjs_biangen_gg","http://www.jl.gov.cn/ggzy/gcjs/bggggc/",["name","ggstart_time","href",'address',"info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.jl.gov.cn/ggzy/gcjs/zbgggc/",["name","ggstart_time","href",'address',"info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.jl.gov.cn/ggzy/zfcg/cggg/",["name","ggstart_time","href",'address',"info"],f1,f2],
    ["zfcg_biangen_gg","http://www.jl.gov.cn/ggzy/zfcg/bggg/",["name","ggstart_time","href",'address',"info"],f1,f2],

    ["zfcg_zhongbiao_gg", "http://www.jl.gov.cn/ggzy/zfcg/zbgg/", ["name", "ggstart_time", "href", 'address', "info"], f1,f2],

    # 单一性来源无法爬取
    # 医药采购数据太少，未爬取
]

def work(conp,**args):
    est_meta(conp,data=data,diqu="吉林省吉林省",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':

    work(conp=["postgres", "since2015", "192.168.3.171", "jilin", "jilin"],num=10)