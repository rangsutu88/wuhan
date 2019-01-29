import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from zhulong.util.etl import est_tbs, est_meta, est_html, est_gg

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_ = 'zhengzhou'


def f1(driver, num):
    locator = (By.XPATH, '//div[@class="List2"]//li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    cnum = re.findall('pageNo=(\d+)', url)[0]

    main_url = url.rsplit('=', maxsplit=1)[0]


    if int(cnum) != num:
        val = driver.find_element_by_xpath('//div[@class="List2"]//li[1]/a').get_attribute('href').rsplit(
            '/', maxsplit=1)[1]

        url_ = main_url + '=%d' % num

        driver.get(url_)

        locator = (By.XPATH, '//div[@class="List2"]//li[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_='List2')
    lis = div.find_all('li')
    for li in lis:
        name = li.a.get_text()
        href = li.a['href']
        if 'http' in href:
            href=href
        else:
            href = "http://www.hngp.gov.cn" + href
        ggstart_time = li.span.get_text()

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//div[@class="List2"]//li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//li[@class="pageInfo"]').text

        total = re.findall('共(.+)页', page)[0].strip()
        total = int(total)
    except:
        total=1
    if total > 300:
        val = driver.find_element_by_xpath('//div[@class="List2"]//li[1]/a').get_attribute('href').rsplit(
            '/', maxsplit=1)[1]
        driver.find_element_by_xpath('//li[@class="lastPage"]/a').click()
        locator = (By.XPATH, '//div[@class="List2"]//li[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            total=driver.find_element_by_xpath('//li[@class="currentPage"]').text.strip()
            total=int(total)
        except:
            total=300
    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@id="content"]')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    locator = (By.XPATH, '//div[@id="content"][string-length()>2] | //div[@id="content"][count(*)>=1]')
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
    div = soup.find('div', id="content")
    div2 = soup.find('div', class_="List1 Top5")
    if div2:
        div = str(div) + str(div2)
        div = BeautifulSoup(div, 'html.parser')
    return div


data = [

     ["zfcg_zhaobiao_diqu1_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=0101&bz=1&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_zhaobiao_diqu2_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=0101&bz=2&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],
    ##包含中标,流标
    ["zfcg_zhong_diqu1_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=0102&bz=1&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_zhong_diqu2_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=0102&bz=2&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

    ##包含变更,流标
    ["zfcg_bian_diqu1_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=0103&bz=1&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_bian_diqu2_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=0103&bz=2&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_danyilaiyuan_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=1301&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_jinkou_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=1302&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

    ##包含预采,其他
    ["zfcg_qita2_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=1303&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_qita_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=1304&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

     ["zfcg_yanshou_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=1402&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

     ["zfcg_jingjia_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=1201&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],
     ["zfcg_jingjia_jieguo_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=1202&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],

     ["zfcg_dingdian_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=1010&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],
     ["zfcg_xieyi_gg", "http://www.hngp.gov.cn/zhengzhou/ggcx?appCode=H61&channelCode=1009&bz=0&pageSize=20&pageNo=1",["name","ggstart_time", "href", 'info'], f1, f2],



]


def work(conp, **args):
    est_meta(conp, data=data, diqu="河南省郑州市", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    conp = ["postgres", "since2015", "192.168.3.171", "lch", "henan_zhengzhou"]

    work(conp=conp)