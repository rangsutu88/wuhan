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


from lch.zhulong import est_tbs,est_meta,est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='leping'

def f1(driver,num):
    locator=(By.XPATH,'//ul[@class="list_news"]/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    if "index.asp" in url:
        cnum=1
    elif not re.findall('index',url):
        cnum=1
    else:
        cnum=int(re.findall("index_([0-9]{1,}).asp",url)[0])
    if num!=cnum:
        if num==1:
            url=re.sub("index[_0-9]*.asp","index.asp",url)
        else:
            s="index_%d.asp"%(num) if num>1 else "index.asp"
            url=re.sub("index[_0-9]*.asp",s,url)
        val=driver.find_element_by_xpath('//ul[@class="list_news"]/li[1]/a').get_attribute('href').rsplit('/',maxsplit=1)[1]
        driver.get(url)
        locator=(By.XPATH,"//ul[@class='list_news']/li[1]/a[not(contains(@href,'%s'))]"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    #
    # rindex = url.rfind('/')
    # main_url = url[:rindex]

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    data=[]
    lis = soup.find('ul', class_='list_news').find_all('li')
    for li in lis:

        name = li.a.get_text()
        href = li.a['href']
        ggstart_time = li.span.get_text()

        if re.findall('http', href):
            href = href
        else:

            href = 'http://www.lpxzfw.gov.cn'+href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//ul[@class="list_news"]/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//div[@class="pagecontent"]/a[last()-2]').text
    except:
        page=1
    total=int(page)
    driver.quit()
    return total



def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@id="infonews"]')

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
    div = soup.find('div',id='infonews')
    return div

data=[

    ["zfcg_gg","http://www.lpxzfw.gov.cn/news/zfcg/",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_gg","http://www.lpxzfw.gov.cn/news/jsgc/",["name","ggstart_time","href",'info'],f1,f2],

    ["zhao_gg","http://www.lpxzfw.gov.cn/news/ZBGG/index.asp",["name","ggstart_time","href",'info'],f1,f2],
    ["zhong_gg","http://www.lpxzfw.gov.cn/news/ZBGS/index.asp",["name","ggstart_time","href",'info'],f1,f2],


]
def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省乐平市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':


    conp=["postgres","since2015","192.168.3.171","jiangxi","leping"]

    work(conp=conp,headless=True)