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


from zhulong.util.etl import est_tbs, est_meta, est_html, est_gg


# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]

#
# url="http://cgb.yantai.gov.cn/col/col12525/index.html?uid=8972&pageNum=1"
# driver=webdriver.Chrome()
# # driver.minimize_window()
# driver.maximize_window()
# driver.get(url)

_name_='yantai'


def f1(driver,num):
    locator = (By.XPATH, '//div[@class="default_pgContainer"]//li[1]/a')
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator))

    url = driver.current_url
    cnum = re.findall('pageNum=(\d+)', url)[0]
    # main_url = url.rsplit('=', maxsplit=1)[0]


    if num != int(cnum):

        # url_ = main_url + '=%d' % num

        val = driver.find_element_by_xpath('//div[@class="default_pgContainer"]//li[1]/a').get_attribute('href')[-25:]

        input_=driver.find_element_by_xpath('//input[@class="default_pgCurrentPage"]')
        input_.clear()
        input_.send_keys(num,Keys.ENTER)

        # driver.get(url_)

        locator = (By.XPATH, '//div[@class="default_pgContainer"]//li[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator))

    ht = driver.page_source
    soup = BeautifulSoup(ht, 'html.parser')
    div = soup.find('div', class_="default_pgContainer")
    uls = div.find_all('li')

    data = []
    for li in uls:
        name = li.a['title']
        href = li.a['href']
        if 'http' in href:
            href = href
        else:
            href = 'http://cgb.yantai.gov.cn' + href
        ggstart_time = li.span.get_text()
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    # with open('chongfu.txt','a',encoding='utf8') as f:
    #     f.write(str(num)+"     "+str(data)+'\n')

    df=pd.DataFrame(data=data)
    df["info"] = None

    return df


def f2(driver):
    locator = (By.XPATH, '//div[@class="default_pgContainer"]//li[1]/a')
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator))

    total = driver.find_element_by_xpath('//span[@class="default_pgTotalPage"]').text
    total=int(total)

    driver.quit()
    return total

def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@id="zoom"] | //table[4]')

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
    div = soup.find('div', id="zoom")
    if div == None:
        div = soup.find('body').find_all('table', recursive=False)[3]
        if div == None:
            raise ValueError



data=[

    ["zfcg_zhaobiao_test_diqu1_gg","http://cgb.yantai.gov.cn/col/col12525/index.html?uid=8972&pageNum=1",["name","ggstart_time","href",'info'],f1,f2],
    # ["zfcg_yucai_diqu1_gg","http://cgb.yantai.gov.cn/col/col12530/index.html?uid=35897&pageNum=1",["name","ggstart_time","href",'info'],f1,f2],
    # ["zfcg_zhongbiao_diqu1_gg","http://cgb.yantai.gov.cn/col/col12526/index.html?uid=8995&pageNum=1",["name","ggstart_time","href",'info'],f1,f2],
    # ["zfcg_biangeng_diqu1_gg","http://cgb.yantai.gov.cn/col/col12527/index.html?uid=9018&pageNum=1",["name","ggstart_time","href",'info'],f1,f2],
    # ["zfcg_yanshou_diqu1_gg","http://cgb.yantai.gov.cn/col/col12529/index.html?uid=35853&pageNum=1",["name","ggstart_time","href",'info'],f1,f2],
    #
    # ["zfcg_zhaobiao_diqu2_gg","http://cgb.yantai.gov.cn/col/col14662/index.html?uid=36255&pageNum=1",["name","ggstart_time","href",'info'],f1,f2],
    # ["zfcg_yucai_diqu2_gg","http://cgb.yantai.gov.cn/col/col14667/index.html?uid=36261&pageNum=1",["name","ggstart_time","href",'info'],f1,f2],
    # ["zfcg_zhongbiao_diqu2_gg","http://cgb.yantai.gov.cn/col/col14663/index.html?uid=36256&pageNum=1",["name","ggstart_time","href",'info'],f1,f2],
    # ["zfcg_biangeng_diqu2_gg","http://cgb.yantai.gov.cn/col/col14664/index.html?uid=36257&pageNum=1",["name","ggstart_time","href",'info'],f1,f2],
    # ["zfcg_yanshou_diqu2_gg","http://cgb.yantai.gov.cn/col/col14666/index.html?uid=36260&pageNum=1",["name","ggstart_time","href",'info'],f1,f2],

]

def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省烟台市",**args)
    # est_html(conp,f=f3,**args)



if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","lch","shandong_yantai"]

    work(conp=conp,headless=False,pageloadtimeout=60,pageloadstrategy='none')