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


# url="http://www.tazfcg.gov.cn/zbcjgs/sjzbcjgs/201505/t20150513_564122.htm"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_ = 'taian'


def f1(driver, num):
    locator = (By.XPATH, '//table[@class="yb14"]//tr[1]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    if 'index.htm' in url:
        cnum = 1
    else:
        cnum = re.findall('index_(\d+)\.htm', url)[0]

    main_url = url.rsplit('/', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//table[@class="yb14"]//tr[1]//a').get_attribute('href').rsplit(
            '/', maxsplit=1)[1]

        if num == 1:
            s = 'index.htm'
        else:
            s = 'index_%d.htm' % (num - 1)
        url_ = re.sub('index_{0,1}(\d*)\.htm', s, url)

        driver.get(url_)

        locator = (By.XPATH, '//table[@class="yb14"]//tr[1]//a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('table', class_='yb14')
    lis = div.find_all('tr')
    for li in lis:
        tds = li.find_all('td')
        href = tds[1].a['href'].strip('.')
        if 'http' in href:
            href = href
        else:
            href = main_url + href
        name = tds[1].a['title']
        ggstart_time = tds[2].get_text()

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//table[@class="yb14"]//tr[1]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//td[@class="out6_td2"]').text
    # print(page)
    total = re.findall('共(\d+)页', page)[0]
    total = int(total)

    driver.quit()
    return total


def f3(driver, url):

    driver.get(url)
    try:
        locator = (By.XPATH, '//div[@class="dbox2"]')

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
    except:
        if '404' in driver.title:
            return 404
        else:
            raise TimeoutError

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
    div = soup.find('div',class_="dbox2")
    if div == None:
        raise ValueError



    return div



data = [

    ["zfcg_yucai_gg", "http://www.tazfcg.gov.cn/cgxqgs/2/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_zhongbiao_diqu1_gg", "http://www.tazfcg.gov.cn/zbcjgs/sjzbcjgs/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_zhongbiao_diqu2_gg", "http://www.tazfcg.gov.cn/zbcjgs/xsqzbcjgs/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_yanshou_gg", "http://www.tazfcg.gov.cn/ysgs/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_biangengliubiao_gg", "http://www.tazfcg.gov.cn/cgbggg/2016n/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],


    ["zfcg_zhaobiao_gongkai_diqu2_gg", "http://www.tazfcg.gov.cn/cggg/xsqcggg/gkzb/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_zhaobiao_gongkai_diqu1_gg", "http://www.tazfcg.gov.cn/cggg/sjcggg/gkzb/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_zhaobiao_yaoqing_diqu2_gg", "http://www.tazfcg.gov.cn/cggg/xsqcggg/yqzb/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_zhaobiao_yaoqing_diqu1_gg", "http://www.tazfcg.gov.cn/cggg/sjcggg/yqzb/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_zhaobiao_xunjia_diqu2_gg", "http://www.tazfcg.gov.cn/cggg/xsqcggg/xj/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_zhaobiao_xunjia_diqu1_gg", "http://www.tazfcg.gov.cn/cggg/sjcggg/xj/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_zhaobiao_danyilaiyuan_diqu2_gg", "http://www.tazfcg.gov.cn/cggg/xsqcggg/dyly/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_zhaobiao_danyilaiyuan_diqu1_gg", "http://www.tazfcg.gov.cn/cggg/sjcggg/dyly/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_zhaobiao_tanpan_diqu1_gg", "http://www.tazfcg.gov.cn/cggg/sjcggg/jzxtp/index.htm",["name","ggstart_time", "href", 'info'], f1, f2],



]


def work(conp, **args):
    est_meta(conp, data=data, diqu="山东省泰安市", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    conp = ["postgres", "since2015", "192.168.3.171", "lch", "shandong_taian"]

    work(conp=conp)