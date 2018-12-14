import time
from os.path import dirname, join

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

from zhulong.util.etl import est_tbs,est_meta,est_html,gg_existed

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="http://ggzyjy.xuancheng.gov.cn/XCTPFront/zfcg/012001/012001001/"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



_name_='xuancheng'


def chang_address(driver,i,c_text,c_type):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]

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
        val = driver.find_element_by_xpath('//tr[@class="trfont"][1]/td[2]/a').get_attribute(
            "href")[- 30:]

        driver.execute_script("window.location.href='./?Paging={}'".format(num))

        locator = (By.XPATH, '//tr[@class="trfont"][1]/td[2]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f1(driver,num):

    #PAGE中包含各个类型页面的总页数
    global PAGE

    locator = (By.XPATH, '//tr[@class="trfont"][1]/td[2]/a')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    c_type = driver.find_element_by_xpath('//div[@class="ewb-now"]/span').text.strip()
    c_text = driver.find_element_by_xpath('//div[@class="l ewb-fwzn"][2]/a').text.strip()

    for i in range(1, int(len(PAGE)) + 1):
        if sum(PAGE[:i - 1]) < num <= sum(PAGE[:i]):
            num = num - sum(PAGE[:i - 1])

            # 增量更新
            if num > CDC_NUM : return
            # if num > 5 : return

            chang_address(driver, i, c_text,c_type)
            chang_page(driver, num)
            is_useful = True
            break

    if 'is_useful' not in locals():
        print('页数不合法%d' % num)
        return

    data = []

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
    global CC_TEXT
    PAGE=[]
    CC_TEXT=[]


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

        cc_text = driver.find_element_by_xpath('//div[@class="l ewb-fwzn"][2]/a').text.strip()
        total_=int(total_)
        PAGE.append(total_)
        CC_TEXT.append(cc_text)
        total = total + total_
    total = int(total)
    driver.quit()

    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//*[@id="form1"]/div[4]/table/tbody/tr/td/table | //div[@class="ewb-main"]')

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

    div = soup.find('div', id="mainContent")
    if div == None:
        div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})
    return div




data=[
    ["gcjs_zhaobiao_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/jsgc/011001/011001001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/jsgc/011001/011001003/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/jsgc/011001/011001004/",["name","ggstart_time","href","info"],f1,f2],

    
    ["zfcg_yvcai_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/zfcg/012001/012001002/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhaobiao_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/zfcg/012001/012001001/",["name","ggstart_time","href","info"],f1,f2],
    #######包含中标流标
    ["zfcg_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/zfcg/012001/012001004/",["name","ggstart_time","href","info"],f1,f2],

    ["qsy_zhaobiao_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/xaxm/022001/022001001/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_biangen_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/xaxm/022001/022001002/",["name","ggstart_time","href","info"],f1,f2],
    ["qsy_zhongbiao_gg","http://ggzyjy.xuancheng.gov.cn/XCTPFront/xaxm/022001/022001004/",["name","ggstart_time","href","info"],f1,f2],

]

def get_profile():
    path1=join(dirname(__file__),'profile')
    with open(path1,'r') as f:
        p=f.read()

    return p

def get_conp(txt):
    x=get_profile() +','+txt
    arr=x.split(',')
    return arr


if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 5
else:
    CDC_NUM = 10000

def work(conp,**args):
    # est_meta(conp,data=data,diqu="安徽省宣城市",**args)
    est_html(conp,f=f3,**args)

# CDC_NUM 为增量更新页数,设置成总页数以上(如:10000)可爬全部
# 增量更新时,需将cdc_total设置成 None


if __name__=='__main__':


    work(conp=["postgres", "since2015", "192.168.3.171", "anhui", "xuancheng"],cdc_total=None)


