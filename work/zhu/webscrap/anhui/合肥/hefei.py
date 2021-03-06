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

from zhulong.util.etl import est_tbs,est_meta,est_html


# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]

#
# url="http://ggzy.hefei.gov.cn/jyxx/002001/002001002/moreinfo_jyxx.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
_name_='hefei'


def f4(driver,num):
    url=driver.current_url
    locator = (By.XPATH, '//*[@id="container"]/div[3]/div/div/div[2]/div[2]/ul/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    if 'moreinfo' in url:
        cnum=1
    else:
        cnum = re.findall('\/(\d+?).html', url)[0]

    main_url = url.rsplit('/', maxsplit=1)[0]
    if int(cnum) != num:
        val = driver.find_element_by_xpath('//*[@id="container"]/div[3]/div/div/div[2]/div[2]/ul/li[1]/a').text
        url = main_url + '/' + str(num) + '.html'

        driver.get(url)

        locator = (By.XPATH, '//*[@id="container"]/div[3]/div/div/div[2]/div[2]/ul/li[1]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    data_ = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    ul=soup.find('ul',class_='ewb-list')
    lis=ul.find_all('li')
    for li in lis:
        address = li.find('span', class_='ewb-label1 l').get_text().strip('】').strip('【')
        href = li.a['href'].strip('.')
        name = li.a.get_text()
        ggstart_time = li.find('span', class_='ewb-list-date r').get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.hefei.gov.cn' + href

        tmp = [address, name, ggstart_time, href]

        data_.append(tmp)
    df = pd.DataFrame(data=data_)
    df['info']=None
    return df


def f1(driver,num):

    locator = (By.XPATH, '/html/body/ul/li[1]/a/span[3]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    if 'moreinfo' in url:
        cnum=1
    else:
        cnum = re.findall('\/(\d+?).html', url)[0]

    main_url = url.rsplit('/', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('/html/body/ul/li[1]/a/span[3]').text
        url = main_url + '/' + str(num) + '.html'

        driver.get(url)

        locator = (By.XPATH, '/html/body/ul/li[1]/a/span[3][not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data_ = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('ul', class_='ewb-right-item')
    lis = div.find_all('li')
    for li in lis:
        address = li.find('span', class_='ewb-label1 l').get_text().strip('】').strip('【')

        href = li.a['href'].strip('.')
        name = li.find('span', class_='ewb-context l').get_text()
        ggstart_time = li.find('span', recursive=False).get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.hefei.gov.cn' + href


        tmp = [address, name, ggstart_time, href]

        data_.append(tmp)
    df=pd.DataFrame(data=data_)
    df['info']=None
    return df


def f2(driver):
    locator = (By.XPATH, '//*[@id="container"]/div[3]/div/div/div[2]/div[2]/ul/li[1]/a | /html/body/ul/li[1]/a/span[3]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//*[@id="index"]').text
        total = re.findall('/(\d+)', page)[0]
        total = int(total)
    except:
        total=1

    driver.quit()
    return total

def f3(driver,url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="ewb-info-bd"]')

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

    div = soup.find('div', class_='ewb-info-bd').find('div',class_='ewb-info-main clearfix')
    if div==None:
        div=soup.find('div',class_="ewb-info-bd")

    return div


data=[
    #
    # ["gcjs_zhaobiao_gg","http://ggzy.hefei.gov.cn/jyxx/002001/002001001/moreinfo_jyxxgg.html",['address', 'name', 'ggstart_time', 'href','info'],f1,f2],
    # ["gcjs_chengqingbiangeng_gg","http://ggzy.hefei.gov.cn/jyxx/002001/002001002/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href','info'],f1,f2],
    # ["gcjs_zhongbiaohx_gg","http://ggzy.hefei.gov.cn/jyxx/002001/002001003/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href','info'],f1,f2],
    # ["gcjs_zhongbiao_gg","http://ggzy.hefei.gov.cn/jyxx/002001/002001004/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href','info'],f1,f2],
    #
    # ["zfcg_zhaobiao_gg","http://ggzy.hefei.gov.cn/jyxx/002002/002002001/moreinfo_jyxxgg.html",['address', 'name', 'ggstart_time', 'href','info'],f1,f2],
    # ["zfcg_dayibiangeng_gg","http://ggzy.hefei.gov.cn/jyxx/002002/002002002/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href','info'],f1,f2],
    # ["zfcg_zhongbiao_gg","http://ggzy.hefei.gov.cn/jyxx/002002/002002004/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href','info'],f1,f2],
    #
    # ["qsy_zhaobiao_gg","http://ggzy.hefei.gov.cn/jyxx/002008/002008001/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href','info'],f1,f2],
    # ["qsy_biangen_gg","http://ggzy.hefei.gov.cn/jyxx/002008/002008002/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href','info'],f1,f2],
    # ["qsy_jieguo_gg","http://ggzy.hefei.gov.cn/jyxx/002008/002008003/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href','info'],f1,f2],

    # ["qsy_dyxly_gg","http://ggzy.hefei.gov.cn/gggs/003003/moreinfo2.html",['address',  'name', 'ggstart_time', 'href','info'],f4,f2],
    ["qsy_yucai_gg","http://ggzy.hefei.gov.cn/gggs/003002/moreinfo2.html",['address',  'name', 'ggstart_time', 'href','info'],f4,f2],

]

# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["postgres","since2015","192.168.3.171","anhui","hefei"]


def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省合肥市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':

    work(conp=["postgres", "since2015", "192.168.3.171", "anhui", "hefei"],html_total=1)

