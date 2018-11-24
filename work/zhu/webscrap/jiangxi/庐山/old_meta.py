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


from  lmfscrap import web

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
from zhulong.util.etl import est_meta, est_html


def f1(driver,num):
    locator=(By.XPATH,'//*[@id="main"]/div[1]/ul/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    cnum=url.rsplit('-',maxsplit=1)[1]
    if str(num) !=cnum:
        url = url.rsplit('-', maxsplit=1)[0] + '-' + str(num)
        val=driver.find_element_by_xpath('//*[@id="main"]/div[1]/ul/li[1]/a').text
        driver.get(url)
        locator=(By.XPATH,"//*[@id='main']/div[1]/ul/li[1]/a[not(contains(string(),'%s'))]"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    uls = soup.find('ul', class_='list')
    data = []
    url = driver.current_url
    rindex = url.rfind('/')
    main_url = url[:rindex]
    lis = uls.find_all('li')

    for li in lis:
        href = li.a['href']
        href = 'http://www.lssggzy.gov.cn' + href
        name = li.a.get_text().strip()
        ggstart_time = li.span.get_text()

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):
    url=driver.current_url
    if url=='http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-45-1':
        total=22
    elif url=='http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-48-1':
        total=81
    elif url=='http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-49-1':
        total=54
    elif url=='http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-52-1':
        total=86
    else:
        total=1
    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="contentxxgk"]')

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
    div = soup.find('div',class_='wzcon fontContent j-fontContent')
    return div

data=[
    #
    ["old_gcjs_zhaobiao_gg","http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-45-1",["name","ggstart_time","href"]],
    ["old_gcjs_zhongbiaohx_gg","http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-48-1",["name","ggstart_time","href"]],

    ["old_zfcg_zhaobiao_gg","http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-49-1",["name","ggstart_time","href"]],
    ["old_zfcg_zhongbiao_gg","http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-52-1",["name","ggstart_time","href"]],


]

def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省庐山市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    # conp=["testor","zhulong","192.168.3.171","test","lch"]
    # conp=["testor","zhulong","192.168.3.171","test","public"]
    conp=["postgres","since2015","192.168.3.171","jiangxi","lushan"]

    work(conp=conp)