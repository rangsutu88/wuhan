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
CC_TEXT=['市级项目','石台县','东至县','青阳县','贵池区']


def chang_address(driver,i,c_text):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]

    if cc_text != c_text:
        driver.find_element_by_xpath(
            '(//font[@color="#17a8e4"])/../../../following-sibling::tr[1]/td/table/tbody/tr[2]/td/a').click()
        locator = (By.XPATH, '(//h4[@class="s-block-title"])[1]/a[2]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath('(//h4[@class="s-block-title"])[{}]/a[2]'.format(i - 1)).click()
        locator = (By.XPATH, '//div[@id="Paging"]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def chang_page(driver,num):
    cnum = driver.find_element_by_xpath('//td[@class="huifont"]').text
    cnum=re.findall('(\d+)/',cnum)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//li[@class="wb-data-list"][1]/div/a').text
        #翻页
        driver.execute_script("window.location.href='./?Paging={}'".format(num))

        locator = (By.XPATH, '//li[@class="wb-data-list"][1]/div/a[not(contains(string(),"{}"))]'.format(val))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f1(driver,num):

    #PAGE中包含各个类型页面的总页数
    global PAGE
    # print(PAGE)

    locator = (By.XPATH, '//li[@class="wb-data-list"][1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    c_text = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/a').text.strip()


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
    lis = soup.find_all('li', class_="wb-data-list")

    for tr in lis:
        href = tr.div.a['href']
        name = tr.div.a['title']
        ggstart_time = tr.span.get_text().strip(']').strip('[')
        if 'http' in href:
            href = href
        else:
            href = "http://ggj.chizhou.gov.cn"+href

        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df



def f2(driver):
    global PAGE

    PAGE=[]
    total=0

    locator = (By.XPATH, '//li[@class="wb-data-list"][1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    for i in range(1, 6):
        if i != 1:
            driver.find_element_by_xpath(
                '(//font[@color="#17a8e4"])/../../../following-sibling::tr[1]/td/table/tbody/tr[2]/td/a').click()
            locator = (By.XPATH, '(//h4[@class="s-block-title"])[1]/a[2]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            driver.find_element_by_xpath('(//h4[@class="s-block-title"])[{}]/a[2]'.format(i - 1)).click()
            locator = (By.XPATH, '//div[@id="Paging"]')
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


    locator = (By.XPATH, '/html/body/div[2]/div/div[2]/div/table/tbody/tr[1]/td/table | //div[@class="ewb-tell-bd"]/table | //*[@id="form1"]/div[4]/div/div[2]/div/table/tbody/tr/td/table')

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
    try:

        div = soup.find('div', class_="ewb-tell-bd").find_all('tr')[2]
    except:
        div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})

    return div




data=[
    ["gcjs_yvcai_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001007/002001007001/",["name","ggstart_time","href","info"],f1,f2],
    # ["gcjs_zhaobiao_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001001/002001001001/",["name","ggstart_time","href","info"],f1,f2],
    # ["gcjs_zhongbiaohx_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001002/002001002001/",["name","ggstart_time","href","info"],f1,f2],
    # ["gcjs_zhongbiao_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001003/002001003001/",["name","ggstart_time","href","info"],f1,f2],
    # ["gcjs_dayibiangeng_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001005/002001005001/",["name","ggstart_time","href","info"],f1,f2],
    #
    # #包含预采和单一性来源
    # ["zfcg_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002005/002002005001/",["name","ggstart_time","href","info"],f1,f2],
    #
    # ["zfcg_zhaobiao_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002001/002002001001/",["name","ggstart_time","href","info"],f1,f2],
    # ["zfcg_liubiao_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002007/002002007001/",["name","ggstart_time","href","info"],f1,f2],
    # ["zfcg_zhongbiao_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002003/002002003001/",["name","ggstart_time","href","info"],f1,f2],
    # #包含答疑和变更
    # ["zfcg_dayibiangeng_gg","http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002004/002002004001/",["name","ggstart_time","href","info"],f1,f2],

]

def work(conp):
    # gg_meta(conp,data=data,diqu="安徽省池州市")

    gg_html(conp,f=f3)


work(conp=["postgres","since2015","192.168.3.171","anhui","chizhou"])