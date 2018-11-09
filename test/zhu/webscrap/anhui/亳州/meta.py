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

#
# url="http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001001/003001001001/003001001001001/"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
#
PAGE=[]
CC_TEXT=['市本级','谯城区','涡阳县','蒙城县','利辛县']


def chang_address(driver,i,c_text):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]

    if cc_text != c_text:

        if i == 2:

            val = driver.find_element_by_xpath(
                '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a').text

            driver.find_element_by_xpath(
                '(//font[@color="red"])[1]/../../../following-sibling::tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/a').click()
            time.sleep(1)
            try:
                driver.execute_script("ShowNewPage('moreinfo.aspx?Paging=1');")
            except:
                driver.execute_script("window.location.href='./moreinfo.aspx?Paging=1'")
            locator = (By.XPATH,
                       '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a[not(contains(string(),"{}"))]'.format(
                           val))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        elif i > 2:
            val = driver.find_element_by_xpath(
                '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a').text

            driver.find_element_by_xpath(
                '(//font[@color="red"])[1]/../../../following-sibling::tr[1]/td/table/tbody/tr[{}]/td/a'.format(
                    i)).click()
            time.sleep(1)
            try:
                driver.execute_script("ShowNewPage('moreinfo.aspx?Paging=1');")
            except:
                driver.execute_script("window.location.href='./moreinfo.aspx?Paging=1'")
            locator = (By.XPATH,
                       '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a[not(contains(string(),"{}"))]'.format(
                           val))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))



def chang_page(driver,num):
    cnum = driver.find_element_by_xpath('//td[@class="huifont"]').text
    cnum=re.findall('(\d+)/',cnum)[0]
    # print(cnum)
    # print(num)

    if num == 1:
        try:
            driver.execute_script("ShowNewPage('moreinfo.aspx?Paging={}');".format(num))
        except:
            driver.execute_script("window.location.href='./moreinfo.aspx?Paging={}'".format(num))

        time.sleep(2)

    if int(cnum) != num:

        val = driver.find_element_by_xpath( '//*[@id="MoreInfoList1_moreinfo"]/tbody/tr/td/table/tbody/tr[1]/'
                                            'td/table/tbody/tr/td[last()-1]/a | '
                                            '//*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a').text


        #翻页,该页面有两种翻页方式
        try:
            driver.execute_script("ShowNewPage('moreinfo.aspx?Paging={}');".format(num))
        except:
            driver.execute_script("window.location.href='./moreinfo.aspx?Paging={}'".format(num))

        locator = (By.XPATH,
                   '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a[not(contains(string(),"{}"))]'.format(val))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f1(driver,num):

    #PAGE中包含各个类型页面的总页数
    global PAGE
    # print(PAGE)

    locator = (By.XPATH,
               '//*[@id="MoreInfoList1_moreinfo"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    c_text = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/font[2]/a[4]/font').text


    if num <= PAGE[0]:
        chang_page(driver,num)

    elif PAGE[0] < num <=sum(PAGE[:2]):

        num=num-PAGE[0]
        chang_address(driver,2,c_text)
        chang_page(driver,num)

    elif sum(PAGE[:2]) < num <= sum(PAGE[:3]):

        num = num - sum(PAGE[:2])
        chang_address(driver, 3,c_text)
        chang_page(driver, num)

    elif sum(PAGE[:3]) < num <= sum(PAGE[:4]):

        num = num - sum(PAGE[:3])
        chang_address(driver, 4,c_text)
        chang_page(driver, num)

    elif sum(PAGE[:4]) < num <= sum(PAGE[:5]):

        num = num - sum(PAGE[:4])
        chang_address(driver, 5,c_text)
        chang_page(driver, num)

    else:
        print('不合法的页数：{}'.format(num))

    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('td', align="right")
    tbody = div.find('tbody')
    trs = tbody.find_all('tr', height='30px', recursive=False)

    for tr in trs:
        table = tr.find('table')
        tds = table.find_all('td')
        href = tds[-2].a['href']
        name = tds[-2].a['title']
        ggstart_time = tds[-1].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.bzztb.gov.cn' + href

        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df



def f2(driver):
    global PAGE

    PAGE=[]
    total=0

    locator = (By.XPATH,
   '//*[@id="MoreInfoList1_moreinfo"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    for i in range(1, 6):
        if i == 1:
            val = driver.find_element_by_xpath(
                '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a').text
            try:
                driver.execute_script("ShowNewPage('moreinfo.aspx?Paging=2');")
            except:
                driver.execute_script("window.location.href='./moreinfo.aspx?Paging=2'")

            locator = (By.XPATH,
                       '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a[not(contains(string(),"{}"))]'.format(
                           val))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


        elif i == 2:
            i = 2
            j = 2
            val = driver.find_element_by_xpath(
                '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a').text

            driver.find_element_by_xpath(
                '(//font[@color="red"])[1]/../../../following-sibling::tr[1]/td/table/tbody/tr[{}]/td/table/tbody/tr[{}]/td/a'.format(
                    i, j)).click()
            time.sleep(1)

            try:
                driver.execute_script("ShowNewPage('moreinfo.aspx?Paging=2');")
            except:
                driver.execute_script("window.location.href='./moreinfo.aspx?Paging=2'")
            locator = (By.XPATH,
                       '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a[not(contains(string(),"{}"))]'.format(
                           val))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        elif i > 2:
            val = driver.find_element_by_xpath(
                '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a').text

            driver.find_element_by_xpath(
                '(//font[@color="red"])[1]/../../../following-sibling::tr[1]/td/table/tbody/tr[{}]/td/a'.format(
                    i)).click()
            time.sleep(1)
            try:
                driver.execute_script("ShowNewPage('moreinfo.aspx?Paging=1');")
            except:
                driver.execute_script("window.location.href='./moreinfo.aspx?Paging=1'")
            locator = (By.XPATH,
                       '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a[not(contains(string(),"{}"))]'.format(
                           val))
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


    locator = (By.XPATH, '//*[@id="tblInfo"]')

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
    div = soup.find('td',class_='infodetail')
    return div




data=[
    ["gcjs_zhaobiao_gg","http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001001/003001001001/003001001001001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001002/003001002001/003001002001001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001004/003001004001/003001004001001/",["name","ggstart_time","href","info"],f1,f2],

    #包含预采和单一性来源
    ["zfcg_zhaobiao_gg","http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002001/003002001001/003002001001001/",["name","ggstart_time","href","info"],f1,f2],
    #包含答疑和变更
    ["zfcg_zhongbiao_gg","http://www.bzztb.gov.cn/BZWZ/jyxx/003002/003002002/003002002001/003002002001001/",["name","ggstart_time","href","info"],f1,f2],
    #其他未爬取
]

def work(conp):
    gg_meta(conp,data=data,diqu="安徽省亳州市")

    gg_html(conp,f=f3)


work(conp=["postgres","since2015","192.168.3.171","anhui","bozhou"])