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

from zhulong.util.etl import est_tbs,est_meta,est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='maanshan'

def f1(driver, num):

    locator = (By.XPATH, '(//font[@class="MoreinfoColor"])[{}]'.format(num))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

    locator = (By.XPATH, '(//tr[@class="TDStylemore"])[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    driver.find_element_by_link_text('更多信息').click()

    locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page_num=driver.find_element_by_xpath('//div[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text

    data_list = []
    for i in range(1,int(page_num) + 1):
        df = f1_data(driver, i)
        data_list.append(df)

    data = []
    for i in data_list:
        for j in i:
            data.append(j)
    df = pd.DataFrame(data=data)
    df["info"] = None

    return df

def f1_data(driver,page):

    if page==1:

        locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    else:
        val = driver.find_element_by_xpath('//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a').text

        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(page))

        locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('table', id='MoreInfoList1_DataGrid1')
    trs = div.find_all('tr', valign='top')

    for tr in trs:
        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a['title']
        ggstart_time = tds[2].get_text().strip()

        if 'http' in href:
            href = href
        else:
            href = 'http://zbcg.mas.gov.cn' + href
        tmp = [name, ggstart_time, href]
        print(tmp)
        data.append(tmp)

    return data




def f2(driver):
    locator = (By.XPATH, '(//td[@class="TDStyle"])[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    total = soup.find_all('font', class_="MoreinfoColor")

    total=len(total)

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
    ["gcjs_zhaobiao_gg","http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_dayibiangeng_gg","http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001002/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001003/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_lingxing_gg","http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001005/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001006/",["name","ggstart_time","href","info"],f1,f2],


    ["zfcg_zhaobiao_gg","http://zbcg.mas.gov.cn/maszbw/jygg/028002/028002001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_dayibiangeng_gg","http://zbcg.mas.gov.cn/maszbw/jygg/028002/028002002/",["name","ggstart_time","href","info"],f1,f2],

    #包含中标流标
    ["zfcg_zhong_gg","http://zbcg.mas.gov.cn/maszbw/jygg/028002/028002002/",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_dyxly_gg","http://zbcg.mas.gov.cn/maszbw/jygg/028002/028002004/",["name","ggstart_time","href","info"],f1,f2],

    ["yucai_gg","http://zbcg.mas.gov.cn/maszbw/jygg/028007/",["name","ggstart_time","href","info"],f1,f2],


]

def work(conp):
    gg_meta(conp,data=data,diqu="安徽省马鞍山市")

    # gg_html(conp,f=f3)


work(conp=["postgres","since2015","192.168.3.171","anhui","maanshan"])