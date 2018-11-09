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

from zhulong.util.etl import gg_meta,gg_html

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="http://www.szggzyjy.cn/szfront/jyxx/002001/002001001/002001001001/"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

PAGE=[]
CC_TEXT=['本级','宣州','郎溪','广德','宁国','泾县','绩溪','旌德']


def chang_address(driver,i,c_text,c_type):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]
    print(cc_text)
    print(c_text)
    print(c_type)
    if cc_text != c_text:
        driver.find_element_by_xpath('//div[@class="l ewb-fwzn"][1]/a').click()
        locator = (By.XPATH, '//*[@id="categorypagingcontent"]/div/div[1]/div/ul/li[1]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath(
  '//li[@class="ewb-menu-item"][{i}]/ul/li/a[contains(string(),"{c_type}")]'.format(i=i,c_type=c_type)).click()
        locator = (By.XPATH, '//tr[@class="trfont"][1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def chang_page(driver,num):
    cnum = driver.find_element_by_xpath('//td[@class="huifont"]').text
    cnum=re.findall('(\d+)/',cnum)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//tr[@class="trfont"][1]/td[2]/a').text

        driver.execute_script("window.location.href='./?Paging={}'".format(num))

        locator = (By.XPATH, '//tr[@class="trfont"][1]/td[2]/a[not(contains(string(),"{}"))]'.format(val))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f1(driver,num):

    #PAGE中包含各个类型页面的总页数
    global PAGE


    locator = (By.XPATH, '//tr[@class="trfont"][1]/td[2]/a')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    c_type = driver.find_element_by_xpath('//div[@class="ewb-now"]/span').text.strip()
    c_text = driver.find_element_by_xpath('//div[@class="l ewb-fwzn"][2]/a').text.strip()


    if num <= PAGE[0]:
        chang_page(driver,num)

    elif PAGE[0] < num <=sum(PAGE[:2]):

        num=num-PAGE[0]
        chang_address(driver,2,c_text,c_type)
        chang_page(driver,num)

    elif sum(PAGE[:2]) < num <= sum(PAGE[:3]):

        num = num - sum(PAGE[:2])
        chang_address(driver, 3,c_text,c_type)
        chang_page(driver, num)

    elif sum(PAGE[:3]) < num <= sum(PAGE[:4]):

        num = num - sum(PAGE[:3])
        chang_address(driver, 4,c_text,c_type)
        chang_page(driver, num)

    elif sum(PAGE[:4]) < num <= sum(PAGE[:5]):

        num = num - sum(PAGE[:4])
        chang_address(driver, 5,c_text,c_type)
        chang_page(driver, num)
    elif sum(PAGE[:5]) < num <= sum(PAGE[:6]):

        num = num - sum(PAGE[:5])
        chang_address(driver, 6,c_text,c_type)
        chang_page(driver, num)
    elif sum(PAGE[:6]) < num <= sum(PAGE[:7]):

        num = num - sum(PAGE[:6])
        chang_address(driver, 7,c_text,c_type)
        chang_page(driver, num)
    elif sum(PAGE[:7]) < num <= sum(PAGE[:8]):

        num = num - sum(PAGE[:7])
        chang_address(driver, 8,c_text,c_type)
        chang_page(driver, num)
    else:
        print('不合法的页数：{}'.format(num))

    data = []
    print(num)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find_all('tr', class_="trfont")

    for tr in trs:
        href = tr.find('td', align='left').a['href']
        name = tr.find('td', align='left').a['title']

        ggstart_time = tr.find('td', align='right').get_text()
        if 'http' in href:
            href = href
        else:
            href = 'http://ggzyjy.xuancheng.gov.cn' + href

        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df



def f2(driver):
    global PAGE

    PAGE=[]


    locator = (By.XPATH, '//tr[@class="trfont"][1]/td[2]/a')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    c_type = driver.find_element_by_xpath('//div[@class="ewb-now"]/span').text.strip()


    total = 0
    for i in range(1, 9):

        if i != 1:
            driver.find_element_by_xpath('//div[@class="l ewb-fwzn"][1]/a').click()
            locator = (By.XPATH, '//*[@id="categorypagingcontent"]/div/div[1]/div/ul/li[1]/a')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            driver.find_element_by_xpath(
      '//li[@class="ewb-menu-item"][{i}]/ul/li/a[contains(string(),"{c_type}")]'.format(i=i,c_type=c_type)).click()
            locator = (By.XPATH, '//tr[@class="trfont"][1]/td[2]/a')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            page = driver.find_element_by_xpath('//td[@class="huifont"]').text
            total_ = re.findall(r'/(\d+)', page)[0]
        except:
            total_ = 0

        total_=int(total_)
        PAGE.append(total_)
        total = total + total_
    total = int(total)
    driver.quit()

    return total


def f3(driver, url):
    driver.get(url)


    locator = (By.XPATH, '//*[@id="form1"]/div[4]/table/tbody/tr/td/table')

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
    div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})
    return div




data=[
    ["gcjs_zhaobiao_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/jsgc/011001/011001001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/jsgc/011001/011001003/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/jsgc/011001/011001004/",["name","ggstart_time","href","info"],f1,f2],


    ["zfcg_yvcai_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/zfcg/012001/012001002/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhaobiao_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/zfcg/012001/012001001/",["name","ggstart_time","href","info"],f1,f2],
    #包含中标流标
    ["zfcg_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/zfcg/012001/012001004/",["name","ggstart_time","href","info"],f1,f2],

    ["qsy_zhaobiao_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/xaxm/022001/022001001/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_biangen_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/xaxm/022001/022001002/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_zhongbiao_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/xaxm/022001/022001004/",["name","ggstart_time","href","info"],f1,f2],

]

def work(conp):
    # gg_meta(conp,data=data,diqu="安徽省宣城市")

    gg_html(conp,f=f3)


work(conp=["postgres","since2015","192.168.3.171","anhui","xuancheng"])