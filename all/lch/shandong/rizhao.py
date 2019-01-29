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

_name_ = 'rizhao'


def f1(driver, num):
    locator = (By.XPATH, '//ul[@id="ctnlist"]/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url=driver.current_url

    cnum = url.rsplit('/', maxsplit=1)[1]
    main_url = url.rsplit('/', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//ul[@id="ctnlist"]/li[1]/a').get_attribute('href')[-10:]

        url_ = main_url + '/%d' % num
        driver.get(url_)

        locator = (By.XPATH, '//ul[@id="ctnlist"]/li[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('ul', id='ctnlist')
    lis = div.find_all('li')
    for td in lis:
        href = td.a['href']
        if 'http' in href:
            href = href
        else:
            href = "http://www.rzzfcg.gov.cn" + href
        name = td.a.get_text()

        ggstart_time = td.span.get_text().strip(']').strip('[')
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//ul[@id="ctnlist"]/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//span[@class="pagesinfo"][2]/b').text

    total = re.findall('/(\d+)', page)[0]
    total = int(total)
    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@id="ctnshow"]')

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
    div = soup.find('div', id="ctnshow")
    return div


data = [

    ["zfcg_zhaobiao_diqu1_gg", "http://www.rzzfcg.gov.cn/ctnlist.php/mid/13/page/1",["name","ggstart_time", "href", 'info'], f1, f2],
    ###包含中标,流标
    ["zfcg_zhong_diqu1_gg", "http://www.rzzfcg.gov.cn/ctnlist.php/mid/15/page/1",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_zhaobiao_diqu2_gg", "http://www.rzzfcg.gov.cn/ctnlist.php/mid/14/page/1",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_zhong_diqu2_gg", "http://www.rzzfcg.gov.cn/ctnlist.php/mid/16/page/1",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_biangeng_gg", "http://www.rzzfcg.gov.cn/ctnlist.php/mid/5/page/1",["name","ggstart_time", "href", 'info'], f1, f2],

    ["zfcg_yucai_diqu1_gg", "http://www.rzzfcg.gov.cn/ctnlist.php/mid/18/page/1",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_yanshou_diqu1_gg", "http://www.rzzfcg.gov.cn/ctnlist.php/mid/20/page/1",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_yucai_diqu2_gg", "http://www.rzzfcg.gov.cn/ctnlist.php/mid/21/page/1",["name","ggstart_time", "href", 'info'], f1, f2],
    ["zfcg_yanshou_diqu2_gg", "http://www.rzzfcg.gov.cn/ctnlist.php/mid/23/page/1",["name","ggstart_time", "href", 'info'], f1, f2],

]


def work(conp, **args):
    est_meta(conp, data=data, diqu="山东省日照市", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    conp = ["postgres", "since2015", "192.168.3.171", "lch", "shandong_rizhao"]

    work(conp=conp,pageloadtimeout=60)