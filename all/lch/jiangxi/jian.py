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


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='jian'


def f1(driver,num):
    locator = (By.XPATH, '//div[@class="moreinfo_list"]//li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    url = driver.current_url

    if 'index.html' in url:
        cnum = 1
    else:
        cnum = int(re.findall("index_(\d+)\.html", url)[0])

    main_url=url.rsplit('/',maxsplit=1)[0]

    if num != cnum:
        s = "index_%d.html" % (num - 1)
        if num == 1:
            url_ = re.sub("index_(\d+)\.html", 'index.html', url)
        else:

            url_ = re.sub("index_{0,1}(\d*)\.html", s, url)

        val = driver.find_element_by_xpath('//div[@class="moreinfo_list"]//li[1]/a').get_attribute('href').rsplit(
            '/', maxsplit=1)[1]

        driver.get(url_)

        locator = (By.XPATH, '//div[@class="moreinfo_list"]//li[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    ht = driver.page_source
    soup = BeautifulSoup(ht, 'html.parser')
    div = soup.find('div', class_="moreinfo_list")
    uls = div.find_all('li')

    data = []
    for li in uls:
        name = li.a.get_text()
        href = li.a['href'].strip('.')
        if 'http' in href:
            href=href
        else:
            href = main_url + href

        ggstart_time = li.span.get_text().strip(']').strip('[')
        tmp = [name, ggstart_time, href]
        data.append(tmp)

    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//div[@class="moreinfo_list"]//li[1]/a')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

    total = driver.find_element_by_xpath('//div[@class="f1"]').text
    total = re.findall('共(.+?)页', total)[0].strip()
    total=int(total)
    driver.quit()
    return total

def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="info_content"]')

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
    div = soup.find('div',class_="info_content")
    return div



data=[

    ["zfcg_zhaobiao_diqu1_gg","http://218.64.81.5/zfcg/sjzbgg/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhaobiao_diqu2_gg","http://218.64.81.5/zfcg/xjzbgg/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhaobiao_xunjia_gg","http://218.64.81.5/zfcg/xjcg/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhongbiao_gg","http://218.64.81.5/zfcg/zbcjgg/index.html",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_xieyi_gg","http://218.64.81.5/zfcg/xygh/index.html",["name","ggstart_time","href",'info'],f1,f2],

]

def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省吉安市",**args)
    est_html(conp,f=f3,**args)



if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","lch","jiangxi_jian"]

    work(conp=conp)