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


_name_='bengbu'

def f1(driver,num):
    locator = (By.XPATH, '//*[@id="DataGrid1"]/tbody/tr[2]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum = driver.find_element_by_xpath('//*[@id="Pager"]/table/tbody/tr/td[1]/font[3]/b').text

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//*[@id="DataGrid1"]/tbody/tr[2]/td[2]/a').text
        driver.execute_script("javascript:__doPostBack('Pager','{}')".format(num))
        locator = (By.XPATH, '//*[@id="DataGrid1"]/tbody/tr[2]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('table', id='DataGrid1')
    trs = div.find_all('tr', valign='top')
    # print(len(trs))

    for tr in trs:
        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a['title']
        ggstart_time = tds[2].get_text().strip()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.bbztb.cn'+href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df




def f2(driver):
    locator = (By.XPATH, '//*[@id="DataGrid1"]/tbody/tr[2]/td[2]/a')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    total = driver.find_element_by_xpath('//*[@id="Pager"]/table/tbody/tr/td[1]/font[2]/b').text

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
    ["gcjs_zhaobiao_gg","http://www.bbztb.cn/bbfwweb/ShowInfo/MoreInfo2.aspx?CategoryNum=003001",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_kongzhijia_gg","http://www.bbztb.cn/bbfwweb/ShowInfo/MoreInfo2.aspx?CategoryNum=026001002",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.bbztb.cn/bbfwweb/ShowInfo/MoreInfo2.aspx?CategoryNum=004001",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://www.bbztb.cn/bbfwweb/ShowInfo/MoreInfo2.aspx?CategoryNum=044",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.bbztb.cn/bbfwweb/ShowInfo/MoreInfo2.aspx?CategoryNum=003002",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_dayibiangeng_gg","http://www.bbztb.cn/bbfwweb/ShowInfo/MoreInfo2.aspx?CategoryNum=026002001",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.bbztb.cn/bbfwweb/ShowInfo/MoreInfo2.aspx?CategoryNum=004002",["name","ggstart_time","href","info"],f1,f2],

    ["qsy_zhaobiao_gg","http://www.bbztb.cn/bbfwweb/ShowInfo/MoreInfo2.aspx?CategoryNum=003006",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_zhongbiao_gg","http://www.bbztb.cn/bbfwweb/ShowInfo/MoreInfo2.aspx?CategoryNum=004006",["name","ggstart_time","href","info"],f1,f2],



]

def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省蚌埠市",**args)
    # est_html(conp,f=f3,**args)

if __name__=='__main__':


    work(conp=["postgres","since2015","192.168.3.171","anhui","bengbu"])