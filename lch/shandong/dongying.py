import random
import time
from collections import OrderedDict

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
from fake_useragent import UserAgent
from zhulong.util.etl import est_tbs, est_meta, est_html, gg_existed, est_gg, add_info

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


url="http://dycg.dongying.gov.cn/BigClassList.aspx?BigClass=1&Zone=5&Type=3"
driver=webdriver.Chrome()
driver.minimize_window()
driver.get(url)


_name_='dongying'

TIME_SLEEP=2

def f1(driver,num):
    global TIME_SLEEP
    ua=UserAgent()

    try:
        locator = (By.XPATH, '(//td[@class="linebottom1"])[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        alert = driver.switch_to.alert
        alert.accept()


    locator = (By.XPATH, '(//td[@class="linebottom1"])[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    url = driver.current_url


    if not locals().get('cnum'):
        cnum=int(driver.find_element_by_xpath('//span[@id="Label1"]').text)
        VIEWSTATE=driver.find_element_by_xpath('//input[@id="__VIEWSTATE"]').get_attribute('value')
        EVENTVALIDATION=driver.find_element_by_xpath('//input[@id="__EVENTVALIDATION"]').get_attribute('value')
        VIEWSTATEGENERATOR=driver.find_element_by_xpath('//input[@id="__VIEWSTATEGENERATOR"]').get_attribute('value')
        content=driver.page_source

    EVENTTARGET_dict={
        'next':'LinkButton4',
        'previou':'LinkButton3',
        'first':'LinkButton2',
        'last':'LinkButton5'
    }

    while cnum != num:
        time.sleep(random.random()+TIME_SLEEP)
        if cnum > num:

            if num < cnum - num:
                mark='first'

            else:
                mark='previou'

        else:
            if total-num < num -cnum:
                mark='last'

            else:
                mark='next'


        form_data={

        "__EVENTTARGET":EVENTTARGET_dict[mark] ,
        "__VIEWSTATE": VIEWSTATE,
        "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
        "__EVENTVALIDATION": EVENTVALIDATION,

        }
        header={
        "Referer": url,
        "User-Agent": ua.chrome,

        }

        req=requests.post(url,data=form_data,headers=header,timeout=15)

        if req.status_code != 200:
            print(req.status_code)

            TIME_SLEEP += 1
            raise ValueError
        content=req.text

        soup = BeautifulSoup(content, 'lxml')
        VIEWSTATE=re.findall('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)" />',content)[0]
        VIEWSTATEGENERATOR=re.findall('<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="(.+?)" />',content)[0]
        EVENTVALIDATION=re.findall('<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.+?)" />',content)[0]
        cnum=int(re.findall('<span id="Label1">(\d+?)</span>',content)[0])

    soup = BeautifulSoup(content, 'lxml')
    tds = soup.find_all('td', class_="linebottom1")
    data = []
    for i in range(0,len(tds),4):

        name =tds[i+1].a.get_text()
        href =tds[i+1].a['href']
        if 'http' in href:
            href=href
        else:
            href = 'http://dycg.dongying.gov.cn/' + href
        ggstart_time = tds[i+3].get_text()
        tmp = [name, ggstart_time, href]
        # print(tmp)
        data.append(tmp)

    df=pd.DataFrame(data=data)

    return df


def f2(driver):
    global total
    try:
        locator = (By.XPATH, '(//td[@class="linebottom1"])[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        alert = driver.switch_to.alert
        alert.accept()

    locator = (By.XPATH, '(//td[@class="linebottom1"])[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    total = driver.find_element_by_xpath('//span[@id="Label2"]').text
    total=int(total)

    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//td[@id="fontzoom"]')

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

    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('td', id="fontzoom")

    return div
def get_data():
    data = []

    ggtype = OrderedDict([("zhaobiao", "1"),("biangengliubiao", "3"), ("zhongbiao", "2")])

    gctype = OrderedDict([('工程','2'),("货物", "1"), ("服务", "3"), ("询价", "4")])

    adtype = OrderedDict([('东营市','5'),("东营区", "6"), ("河口区", "7"), ("广饶县", "8"), ("垦利县", "9"),
                          ("利津县", "10"),("开发区", "11"),("东营港", "12"),("农高区", "13")])

    for w1 in ggtype.keys():
        for w2 in adtype.keys():
            for w3 in gctype.keys():
                href="http://dycg.dongying.gov.cn/BigClassList.aspx?BigClass={gc}&Zone={ad}&Type={gg}".format(gc=gctype[w3],gg=ggtype[w1],ad=adtype[w2])
                tmp=["zfcg_%s_diqu%s_type%s_gg"%(w1,adtype[w2],gctype[w3]),href,["name","ggstart_time","href",'info'],add_info(f1,{"jy_type":w3,"diqu":w2}),f2]

                data.append(tmp)

    remove_arr = ["zfcg_biangengliubiao_diqu9_type2_gg"]
    data1 = data.copy()
    for w in data:
        if w[0] in remove_arr: data1.remove(w)


    return data1

data=get_data()

def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省东营市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","lch","shandong_dongying"]

    work(conp=conp,pageloadstrategy='none',pageloadtimeout=60)