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

_name_='ningxia'

def f1(driver,num):
    locator = (By.XPATH, '//ul[@id="showList"]/ul/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    cnum = re.findall('/(\d+)\.html', url)[0]

    if int(cnum) != num:
        main_url = url.rsplit('/', maxsplit=1)[0]
        val = driver.find_element_by_xpath('//ul[@id="showList"]/ul/li[1]/div/a').text

        url = main_url + '/' + str(num) + '.html'

        driver.get(url)

        locator = (By.XPATH, '//ul[@id="showList"]/ul/li[1]/div/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('ul', id='showList').find('ul')
    lis = div.find_all('li')

    for li in lis:
        if li.find('font', color="#FF0000"): li.find('font', color="#FF0000").extract()
        href = li.div.a['href']
        name = li.div.a.get_text()
        ggstart_time = li.find('span', class_='ewb-date').get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.nxggzyjy.org' + href

        tmp = [name, href, ggstart_time]
        data.append(tmp)

    df=pd.DataFrame(data=data)
    df['info']=None
    return df



def f2(driver):
    locator = (By.XPATH, '//ul[@id="showList"]/ul/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//li[@id="index"]').text
    page=re.findall('/(\d+)',page)[0]
    total=int(page)
    driver.quit()
    return total

def f3(driver, url):
    driver.get(url)
    try:
        locator = (By.XPATH, '//div[@style="display: block;"] | //div[@data-role="body"] | //div[@class="ewb-main"]')

        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        if '404' in driver.title:

            return  404
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

    soup = BeautifulSoup(page, 'lxml')
    div = soup.find('div',style='display: block;')
    if div == None:
        div= soup.find('div',attrs={'data-role':"body"})
        if div == None:
            div=soup.find('div',class_='ewb-main')

    return div

data=[

    ["gcjs_zhaobiao_gg","http://www.nxggzyjy.org/ningxiaweb/002/002001/002001001/1.html",[ "name", "href", "ggstart_time","info"],f1,f2],
    ["gcjs_biangengdayi_gg","http://www.nxggzyjy.org/ningxiaweb/002/002001/002001002/1.html",[ "name", "href", "ggstart_time","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.nxggzyjy.org/ningxiaweb/002/002001/002001003/1.html",[ "name", "href", "ggstart_time","info"],f1,f2],

    ["zfcg_zhaobiao_gg","http://www.nxggzyjy.org/ningxiaweb/002/002002/002002001/1.html",[ "name", "href", "ggstart_time","info"],f1,f2],
    ["zfcg_biangengdayi_gg","http://www.nxggzyjy.org/ningxiaweb/002/002002/002002002/1.html",[ "name", "href", "ggstart_time","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.nxggzyjy.org/ningxiaweb/002/002002/002002003/1.html",[ "name", "href", "ggstart_time","info"],f1,f2],

    ["yycg_zhaobiao_gg","http://www.nxggzyjy.org/ningxiaweb/002/002003/002003001/1.html",[ "name", "href", "ggstart_time","info"],f1,f2],
    #包含中标,其他
    ["yycg_zhong_gg","http://www.nxggzyjy.org/ningxiaweb/002/002003/002003002/1.html",[ "name", "href", "ggstart_time","info"],f1,f2],



]

def work(conp,**args):
    # est_meta(conp,data=data,diqu="宁夏回族自治区宁夏",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","ningxia","ningxia"]

    work(conp=conp,num=10,)