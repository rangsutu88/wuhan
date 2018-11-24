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


# url="http://www.hbzbcg.cn/hbweb/jyxx/002001/002001001/002001001001/MoreInfo.aspx?CategoryNum=002001001001"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

page_one=0

def f1(driver,num):

    #记录第一种情况的总页码
    global page_one

    locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum_text = driver.find_element_by_xpath('//div[@class="main3"]/table/tbody/tr/td[3]/'
                                             'table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/font[2]/a[4]/font').text
    if cnum_text=='市本级':
        page_one = driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text



    if num <= int(page_one):
        cnum=driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text
        if int(cnum) != num:
            val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
            driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))

            locator = (
            By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    elif int(page_one) < num:
        num=num-int(page_one)
        print(num)

        cnum_text=driver.find_element_by_xpath('//div[@class="main3"]/table/tbody/tr/td[3]/'
                                               'table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/font[2]/a[4]/font').text
        if cnum_text=='市本级':
            driver.find_element_by_xpath('//div[@class="main3"]/table/tbody/tr/td[3]/table/tbody/tr[1]/'
                                         'td[2]/table/tbody/tr/td[2]/font[2]/a[3]').click()
            locator = (By.XPATH, '//*[@id="container"]/div[4]/table/tbody/tr/td[3]/table/tbody/tr[2]/'
                                 'td/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[2]/a')

            #返回公告分类页等待
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            driver.find_element_by_xpath('//*[@id="container"]/div[4]/table/tbody/tr/td[3]/table/tbody/'
                                         'tr[2]/td/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[3]/a').click()
            #进入濉溪县页面等待
            locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

            #等于1不需要翻页
            if num !=1:
                val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
                driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))
                #翻页等待
                locator = (
                    By.XPATH,
                    '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        elif cnum_text=='濉溪县':
            cnum = driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text
            if int(cnum) != num:
                val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
                driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))

                locator = (
                    By.XPATH,
                    '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('table', id='MoreInfoList1_DataGrid1')
    trs = div.find_all('tr', valign='top')
    print(len(trs))

    for tr in trs:
        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a['title']
        if '</font>' in name:
            name = re.findall(r'</font>(.+)', name)[0]
        ggstart_time = tds[2].get_text().strip()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.hbzbcg.cn' + href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df




def f2(driver):
    url = driver.current_url
    print(url)
    new_url=re.findall('http://www.hbzbcg.cn/hbweb/jyxx/\d+?/\d+?/',url)[0]
    print(new_url)
    driver.get(new_url)
    locator = (By.XPATH, '(//td[@class="TDStyle"])[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    more_num = soup.find_all('font', class_="MoreinfoColor")
    more = len(more_num)
    total=0
    for num in range(1,more+1):
        driver.get(new_url)
        locator = (By.XPATH, '(//font[@class="MoreinfoColor"])[{}]'.format(num))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        total_=driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text
        total += int(total_)
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
    ["gcjs_zhaobiao_gg","http://www.hbzbcg.cn/hbweb/jyxx/002001/002001001/002001001001/MoreInfo.aspx?CategoryNum=002001001001",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_dayibiangeng_gg","http://www.hbzbcg.cn/hbweb/jyxx/002001/002001003/002001003001/MoreInfo.aspx?CategoryNum=002001003001",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.hbzbcg.cn/hbweb/jyxx/002001/002001005/002001005001/MoreInfo.aspx?CategoryNum=002001005001",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://www.hbzbcg.cn/hbweb/jyxx/002001/002001002/002001002001/MoreInfo.aspx?CategoryNum=002001002001",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.hbzbcg.cn/hbweb/jyxx/002002/002002001/002002001001/MoreInfo.aspx?CategoryNum=002002001001",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_dayibiangeng_gg","http://www.hbzbcg.cn/hbweb/jyxx/002002/002002003/002002003001/MoreInfo.aspx?CategoryNum=002002003001",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.hbzbcg.cn/hbweb/jyxx/002002/002002002/002002002001/MoreInfo.aspx?CategoryNum=002002002001",["name","ggstart_time","href","info"],f1,f2],


]

def work(conp):
    gg_meta(conp,data=data,diqu="安徽省淮北市")

    gg_html(conp,f=f3)


work(conp=["postgres","since2015","192.168.3.171","anhui","huaibei"])