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

PAGE=[]

def chang_address(driver,i,c_text):

    # 不是对应的的都要点击
    cc_text=driver.find_element_by_xpath(
        '(//td[@class="LeftMenuSubbg" and not(@style)])[last()]/table/tbody/tr[{}]/td/a'.format(i)).text
    cc_text=re.findall('(.+)>>',cc_text)[0]
    if cc_text != c_text:
        val = driver.find_element_by_xpath(
            '//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a').text
        driver.find_element_by_xpath(
            '(//td[@class="LeftMenuSubbg" and not(@style)])[last()]/table/tbody/tr[{}]/td/a'.format(i)).click()
        locator = (By.XPATH,
                   '//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def chang_page(driver,num):
    cnum = driver.find_element_by_xpath('//td[@class="huifont"]').text
    cnum=re.findall('(\d+)/',cnum)[0]

    #第一页不用翻页
    if int(cnum) != num:
        val = driver.find_element_by_xpath(
            '//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a').text

        driver.execute_script("window.location.href='./?Paging={}'".format(num))
        # 第二个等待
        locator = (By.XPATH,
                   '//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

def f1(driver,num):

    #PAGE中包含各个类型页面的总页数
    global PAGE
    # print(PAGE)

    locator = (By.XPATH, '//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    c_text = driver.find_element_by_xpath('//div[@class="right-wrap-head"]/table/tbody/tr/td[2]/font[2]/a[4]').text


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

    elif sum(PAGE[:5]) < num <= sum(PAGE[:6]):

        num = num - sum(PAGE[:5])
        chang_address(driver, 6,c_text)
        chang_page(driver, num)

    elif sum(PAGE[:6]) < num <= sum(PAGE[:7]):

        num = num - sum(PAGE[:6])
        chang_address(driver, 7,c_text)
        chang_page(driver, num)

    elif sum(PAGE[:7]) < num <= sum(PAGE[:8]):

        num = num - sum(PAGE[:7])
        chang_address(driver, 8,c_text)
        chang_page(driver, num)

    elif sum(PAGE[:8]) < num <= sum(PAGE[:9]):

        num = num - sum(PAGE[:8])
        chang_address(driver, 9,c_text)
        chang_page(driver, num)
    else:
        print('不合法的页数：{}'.format(num))


    data = []
    # print(num)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_='right-wrap-ccontent-text')
    trs = div.find_all('tr', height=25)
    # print(len(trs))
    for tr in trs:
        href = tr.find('td', align='left').a['href']
        name = tr.find('td', align='left').a['title']
        ggstart_time = tr.find('td', align='right').get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.czggzy.gov.cn' + href

        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df




def f2(driver):
    global PAGE

    PAGE=[]
    locator = (By.XPATH, '//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    total = 0
    for i in range(1, 10):
        if i != 1:
            val = driver.find_element_by_xpath(
                '//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a').text
            driver.find_element_by_xpath(
                '(//td[@class="LeftMenuSubbg" and not(@style)])[last()]/table/tbody/tr[{}]/td/a'.format(i)).click()
            locator = (By.XPATH,
                       '//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        try:
            page = driver.find_element_by_xpath('//td[@class="huifont"]').text

            total_ = re.findall(r'/(\d+)', page)[0]
        except:
            total_ = 0
        total_=int(total_)
        PAGE.append(total_)

        total = total + int(total_)
    total = int(total)
    driver.quit()

    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '/html/body/div[2]/div/div/div[2]/table')

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

    div = soup.find('div', attrs={'id': re.compile('menutab_5_\d'), 'style': ''})

    return div





data=[
    # ["gcjs_zhaobiao_gg","http://www.czggzy.gov.cn/Front_jyzx/jyxx/002008/002008001/002008001001/",["name","ggstart_time","href","info"],f1,f2],
    # ["gcjs_zhongbiaohx_gg","http://www.czggzy.gov.cn/Front_jyzx/jyxx/002008/002008003/002008003001/",["name","ggstart_time","href","info"],f1,f2],
    # ["gcjs_zhongbiao_gg","http://www.czggzy.gov.cn/Front_jyzx/jyxx/002008/002008004/002008004001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_liubiao_gg","http://www.czggzy.gov.cn/Front_jyzx/jyxx/002008/002008006/002008006001/",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.czggzy.gov.cn/Front_jyzx/jyxx/002009/002009001/002009001001/",["name","ggstart_time","href","info"],f1,f2],
    #框架暂定变更为biangen
    ["zfcg_biangen_gg","http://www.czggzy.gov.cn/Front_jyzx/jyxx/002009/002009002/002009002001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.czggzy.gov.cn/Front_jyzx/jyxx/002009/002009003/002009003001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_liubiao_gg","http://www.czggzy.gov.cn/Front_jyzx/jyxx/002009/002009005/002009005001/",["name","ggstart_time","href","info"],f1,f2],



]

def work(conp):
    gg_meta(conp,data=data,diqu="安徽省滁州市")

    # gg_html(conp,f=f3)


work(conp=["postgres","since2015","192.168.3.171","anhui","chuzhou"])