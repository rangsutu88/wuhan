import time

import pandas as pd
import re

from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

from zhulong.util.etl import add_info,est_meta,est_html,est_tbs

from collections import OrderedDict


_name_="shenghui"


def f1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    locator = (By.XPATH, '(//div[@class="ewb-info-a"]/a)[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    if "about.html" in url:
        cnum=1
    else:
        cnum=int(re.findall("/([0-9]{1,}).html", url)[0])
    if num!=cnum:
        if num==1:
            url=re.sub("[0-9]*.html","about.html",url)
        else:
            s = "%d.html" % (num) if num > 1 else "index.html"
            url = re.sub("about[0-9]*.html", s, url)
            # print(cnum)
        val = driver.find_element_by_xpath("(//div[@class='ewb-info-a']/a)[1]").text
        # print(url)
        driver.get(url)
        time.sleep(2)

        locator = (By.XPATH, "(//div[@class='ewb-info-a']/a)[1][string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("ul", class_="ewb-info-items")

    lis = ul.find_all("li", class_="ewb-info-item clearfix")
    data = []
    for li in lis:
        a = li.find("a")
        link = "http://www.sdsggzyjyzx.gov.cn" + a["href"]
        span = li.find("span", class_="ewb-date")
        tmp = [a.text.strip(), span.text.strip(), link]
        data.append(tmp)

    df = pd.DataFrame(data=data)
    df["info"]=None
    return df


def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    try:
        locator = (By.XPATH, '//*[@id="index"]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall('/(.*)', page_all)[0]
        # print(page)
    except Exception as e:
        page = "1"
    driver.quit()
    return int(page)

def f3(driver,url):


    driver.get(url)

    locator=(By.CLASS_NAME,"news-detail-wrap")

    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located(locator))

    before=len(driver.page_source)
    time.sleep(0.1)
    after=len(driver.page_source)
    i=0
    while before!=after:
        before=len(driver.page_source)
        time.sleep(0.1)
        after=len(driver.page_source)
        i+=1
        if i>5:break

    page=driver.page_source

    soup=BeautifulSoup(page,'lxml')

    div=soup.find('div',class_='news-detail-wrap')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div



data = [
        ["zfcg_caigoudongtai_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002001/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_caigou_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002002/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_biangeng_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002003/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_zhongbiao_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002004/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["ylcg_yaopincaigou_tongzhi_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004001/069004001001/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["ylcg_yaopincaigou_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004001/069004001002/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["ylcg_yaopincaigou_geshicaigou_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004001/069004001003/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["ylcg_haocaicaigou_tongzhi_gg","http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004002/069004002001/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["ylcg_haocaicaigou_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004002/069004002002/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["ylcg_yimiaocaigou_tongzhi_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004003/069004003001/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["ylcg_yimiaocaigou_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004003/069004003002/about.html",
         ["name", "ggstart_time", "href","info"],f1,f2],

    ]



def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省省会",num=5)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","shenghui"])

#est_tbs(conp=["postgres","since2015","127.0.0.1","shandong","shenghui"],data=data,total=1,num=1)