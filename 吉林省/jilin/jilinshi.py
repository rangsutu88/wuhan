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

from zhulong.util.etl import est_tbs, est_meta, est_html, gg_existed

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]

# #
# url="http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001001/003001001001/"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


_name_='jilinshi'

def chang_address(driver,i,c_text):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]

    if cc_text != c_text:
        driver.find_element_by_xpath('//div[@class="ewb-right-hd"]/a[4]').click()
        locator = (By.XPATH, '//div[@id="categorypagingcontent"]/div[1]/div[1]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath('//div[@id="categorypagingcontent"]/div[{}]/div[1]/a'.format(i)).click()

        locator = (By.XPATH, '//*[@id="categorypagingcontent"]/div/div/div[2]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))



def chang_page(driver,num):
    try:
        cnum = driver.find_element_by_xpath('//li[@class="wb-page-li"][last()-1]/a').text.strip()

        cnum = re.findall('(\d+)/', cnum)[0]
    except:
        cnum='1'
    if cnum != str(num):
        val = driver.find_element_by_xpath('//ul[@class="ewb-com-items"]/li[1]/div/a').text

        driver.execute_script("ShowAjaxNewPage(window.location.pathname,'categorypagingcontent',{})".format(num))

        locator = (By.XPATH, '//ul[@class="ewb-com-items"]/li[1]/div/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))



def f1(driver,num):

    #PAGE中包含各个类型页面的总页数

    locator = (By.XPATH, '//ul[@class="ewb-com-items"]/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    c_text = driver.find_element_by_xpath('//div[@class="ewb-right-hd"]/span').text

    for i in range(1, int(len(PAGE)) + 1):
        if sum(PAGE[:i - 1]) < num <= sum(PAGE[:i]):
            num = num - sum(PAGE[:i - 1])

            # 增量更新
            if num > CDC_NUM : return

            chang_address(driver, i, c_text)
            chang_page(driver, num)
            is_useful = True
            break

    if 'is_useful' not in locals():
        print('页数不合法%d' % num)
        return


    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('ul', class_='ewb-com-items')
    trs = div.find_all('li')

    for tr in trs:
        href = tr.div.a['href']
        name = tr.div.a.get_text()
        ggstart_time = tr.span.get_text().strip()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.jlsggzyjy.gov.cn' + href

        tmp = [name, ggstart_time, href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df



def f2(driver):
    global PAGE
    global CC_TEXT
    PAGE=[]
    CC_TEXT = []
    locator = (By.XPATH, '//ul[@class="ewb-com-items"]/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    for i in range(1,7):
        if i != 1:
            driver.find_element_by_xpath('//div[@class="ewb-right-hd"]/a[4]').click()
            locator=(By.XPATH,'//div[@id="categorypagingcontent"]/div[1]/div[1]/a')
            WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
            driver.find_element_by_xpath('//div[@id="categorypagingcontent"]/div[{}]/div[1]/a'.format(i)).click()

            locator=(By.XPATH,'//*[@id="categorypagingcontent"]/div/div/div[2]')
            WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

        try:
            page = driver.find_element_by_xpath('//li[@class="wb-page-li"][last()-1]/a').text
            total_ = int(re.findall('/(\d+)', page)[0])
        except:
            html=driver.page_source
            if '本栏目暂无信息' in html:
                total_=0
            else:
                total_=1
        cc_text=driver.find_element_by_xpath('//div[@class="ewb-right-hd"]/span').text
        PAGE.append(total_)
        CC_TEXT.append(cc_text)

    total = sum(PAGE)
    driver.quit()

    return total




def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="ewb-right"]')

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
    div = soup.find('div',id='mainContent')
    return div




data=[
    ["gcjs_zhaobiao_gg","http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001001/003001001001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_biangenliubiao_gg","http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001002/003001002001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001003/003001003001/",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001004/003001004001/",["name","ggstart_time","href","info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003002/003002001/003002001001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_biangenliubiao_gg","http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003002/003002002/003002002001/",["name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003002/003002003/003002003001/",["name","ggstart_time","href","info"],f1,f2],

]


def get_profile():
    path1 = join(dirname(__file__), 'profile')
    with open(path1, 'r') as f:
        p = f.read()

    return p


def get_conp(txt):
    x = get_profile() + ',' + txt
    arr = x.split(',')
    return arr


if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 5
else:
    CDC_NUM = 10000


def work(conp,**args):
    est_meta(conp,data=data,diqu="吉林省吉林市",**args)
    est_html(conp,f=f3,**args)

# CDC_NUM 为增量更新页数,设置成总页数以上(如:10000)可爬全部
# 增量更新时,需将cdc_total设置成 None


if __name__=='__main__':


    work(conp=["postgres","since2015","192.168.3.171","jilin","jilinshi"],cdc_total=None)