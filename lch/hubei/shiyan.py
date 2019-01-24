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

_name_='shiyan'


def f1(driver,num):
    locator = (By.XPATH, '//ul[@class="gl_list"][1]/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    url = driver.current_url

    if 'index.shtml' in url:
        cnum = 1
    else:
        cnum = int(re.findall("index_(\d+)\.shtml", url)[0]) + 1

    main_url = url.rsplit('/', maxsplit=1)[0]

    if num != cnum:
        s = "index_%d.shtml" % (num-1)
        if num == 1:
            url_ = re.sub("index_(\d+)\.shtml", 'index.shtml', url)
        else:
            url_ = re.sub("index_{0,1}(\d*)\.shtml", s, url)

        val = driver.find_element_by_xpath('//ul[@class="gl_list"][1]/li[1]/a').get_attribute('href').rsplit(
            '/', maxsplit=1)[1]

        driver.get(url_)

        locator = (By.XPATH, '//ul[@class="gl_list"][1]/li[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    ht = driver.page_source
    soup = BeautifulSoup(ht, 'lxml')
    div = soup.find('div', class_="zcgl_right")
    uls = div.find_all('li')

    data = []
    for li in uls:
        name = li.a['title']
        href = li.a['href'].strip('.')
        if 'http' in href:
            href = href
        else:
            href = main_url + href
        ggstart_time = li.find('span').get_text().strip()
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//ul[@class="gl_list"][1]/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    try:
        driver.find_element_by_xpath('//div[@class="page"]/div/a[last()]')
    except:
        driver.quit()
        return 1

    while True:
        val = driver.find_element_by_xpath('//ul[@class="gl_list"][1]/li[1]/a').get_attribute('href').rsplit(
            '/', maxsplit=1)[1]

        driver.find_element_by_xpath('//div[@class="page"]/div/a[last()-1]').click()
        locator = (By.XPATH, '//ul[@class="gl_list"][1]/li[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        mark = driver.find_element_by_xpath('//div[@class="page"]/div/a[last()]').text.strip()

        if mark != '>':
            break

    total = driver.find_element_by_xpath('//span[@class="current"]').text.strip()

    total = int(total)

    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@id="Zoom"]')

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
    div = soup.find('div',id="Zoom")
    return div




data=[

    ["zfcg_zhaobiao_gongkai_gg","http://cgzx.shiyan.gov.cn/bxxx/cgxx_30986/gkzb/index.shtml",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhaobiao_cuoshang_gg","http://cgzx.shiyan.gov.cn/bxxx/cgxx_30986/jzxcs/index.shtml",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhaobiao_tanpan_gg","http://cgzx.shiyan.gov.cn/bxxx/cgxx_30986/jzxtp/index.shtml",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhaobiao_xunjia_gg","http://cgzx.shiyan.gov.cn/bxxx/cgxx_30986/xj/index.shtml",["name","ggstart_time","href",'info'],f1,f2],

    ["zfcg_biangeng_gg","http://cgzx.shiyan.gov.cn/bxxx/cgxx_30986/gzgg/index.shtml",["name","ggstart_time","href",'info'],f1,f2],

    ["zfcg_jieguo1_gg","http://cgzx.shiyan.gov.cn/bxxx/cjxx_30994/zbgg/index.shtml",["name","ggstart_time","href",'info'],f1,f2],
    ##包含流标,中标
    ["zfcg_jieguo2_gg","http://cgzx.shiyan.gov.cn/bxxx/cjxx_30994/cjgg/index.shtml",["name","ggstart_time","href",'info'],f1,f2],

    ["zfcg_jieguobiangeng_gg","http://cgzx.shiyan.gov.cn/bxxx/cjxx_30994/gzgg_cj/index.shtml",["name","ggstart_time","href",'info'],f1,f2],

]

def work(conp,**args):
    est_meta(conp,data=data,diqu="湖北省十堰市",**args)
    est_html(conp,f=f3,**args)
    # est_gg(conp,diqu="湖北省十堰市")



if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","lch","hubei_shiyan"]

    work(conp=conp,headless=False,pageloadtimeout=60,pageloadstrategy='none')