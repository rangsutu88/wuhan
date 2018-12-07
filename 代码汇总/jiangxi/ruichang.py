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


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='ruichang'

def f1(driver,num):
    locator=(By.XPATH,'/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[3]/tbody/tr[2]/td[1]/div')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    if "index.htm" in url:
        cnum=1
    else:
        cnum=int(re.findall("index_([0-9]{1,}).htm",url)[0])+1
    if num!=cnum:
        if num==1:
            url=re.sub("index[_0-9]*.html","index.htm",url)
        else:
            s="index_%d.htm"%(num-1) if num>1 else "index.htm"
            url=re.sub("index[_0-9]*.htm",s,url)

        val = driver.find_element_by_xpath('/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[5]/tbody/tr/td/div').text
        driver.get(url)
        locator = (By.XPATH,
                   '/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[3]/tbody/tr[2]/td[1]/div[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find_all('tr', bgcolor='#FFFFFF')

    for i in range(1, len(trs)):
        tr = trs[i]
        tds = tr.find_all('td')
        index_num = tds[0].div.get_text()
        index_num = re.findall("xxsqh=\'(.+?)\';", index_num)[0]

        status = tds[1].div.div.get_text()
        href = tds[2].div.div.a['href'].strip('.')
        name = tds[2].div.div.a.get_text()
        gksj = tds[3].div.div.get_text()
        gkfw = tds[4].div.div.get_text()
        ggstart_time = tds[5].div.div.get_text()

        if 'http' in href:
            href = href
        else:
            href = url + href

        tmp = [index_num, status, gksj, gkfw, name,  ggstart_time,href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (
    By.XPATH, '/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[3]/tbody/tr[2]/td[1]/div')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath(
        '/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[5]/tbody/tr/td/div').text

    total = re.findall('总共(\d+?)页', page)[0]
    total=int(total)
    driver.quit()
    return total

def f3(driver, url):
    driver.get(url)
    try:
        locator = (By.XPATH, '//div[@id="article"]')

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
    except:
        title=driver.title
        if '404' in title:
            return
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
    div = soup.find('div',id="article")
    return div


data=[

    ["zfcg_gg","http://218.65.3.188/rcs/cjxx/zfcgyztb/index.htm",['index_num','type','gksj','gkfw',"name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_gg","http://218.65.3.188/rcs/gddt/gggs/index.htm",['index_num','type','gksj','gkfw',"name","ggstart_time","href",'info'],f1,f2],

]

def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省瑞昌市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':


    conp=["postgres","since2015","192.168.3.171","jiangxi","ruichang"]

    work(conp=conp)