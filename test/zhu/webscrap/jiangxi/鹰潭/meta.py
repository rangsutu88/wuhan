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


from  lmfscrap import web

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]

#
# url="http://www.yingtan.gov.cn/xxgk/zdgc/zdgcztb/index.htm"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
def general_template(tb,url,col,conp):

    m=web()
    setting={
    "url":url,
    "f1":f1,
    "f2":f2,
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":8,
        # 'total':5


    }
    m=web()
    m.write(**setting)


def f1(driver,num):
    locator=(By.XPATH,"//div[@class='ldjs_body']/ul/li/a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    if "index.htm" in url:
        cnum=1
    else:
        cnum=int(re.findall("index_([0-9]{1,}).htm",url)[0])+1
    if num!=cnum:
        if num==1:
            url=re.sub("index[_0-9]*.htm","index.htm",url)
        else:
            s="index_%d.htm"%(num-1) if num>1 else "index.htm"
            url=re.sub("index[_0-9]*.htm",s,url)
        val=driver.find_element_by_xpath("//div[@class='ldjs_body']/ul/li/a").text
        driver.get(url)
        locator=(By.XPATH,"//div[@class='ldjs_body']/ul/li/a[not(contains(string(),'%s'))]"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    page = driver.page_source

    soup = BeautifulSoup(page, "lxml")
    url = driver.current_url
    rindex = url.rfind('/')
    url_1 = url[:rindex]
    url_2 = re.findall('http://www.yingtan.gov.cn/\w+?/', url)[0]
    # print(url_2)
    tables = soup.find('div', class_='ldjs_body')
    lis = tables.find_all('li')
    data = []
    for i in range(0, len(lis), 2):
        # print(li)
        li = lis[i]
        href = li.a['href'].strip('.')
        # print(href)
        title = li.get_text().strip().strip('•').strip()
        li = lis[i + 1]
        data_time = li.get_text().strip()
        if re.findall('http', href):
            href = href
        elif re.findall(r'/\.\./', href):
            href = href.split(r'/../')[1]
            href = url_2 + href
        else:
            href = url_1 + href


        tmp = [title, data_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):

    locator = (By.XPATH, "//div[@class='ldjs_body']/ul/li/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page = driver.find_element_by_xpath("(//*[@class='cn'])[5]").text
    total = re.findall('总共(\d+)页', page)[0]
    total=int(total)
    return total

def work(conp,i=-1):
    data=[

        ["gcjs_zhaobiao_gg","http://www.yingtan.gov.cn/xxgk/zdgc/zdgcztb/index.htm",["name","ggstart_time","href"]],
        ["zfcg_zhaobiao_gg","http://www.yingtan.gov.cn/xxgk/zfcg/zhaobgg/index.htm",["name","ggstart_time","href"]],
        ["zfcg_zhongbiao_gg","http://www.yingtan.gov.cn/xxgk/zfcg/zbgg/index.htm",["name","ggstart_time","href"]],
        ["zfcg_liubiao_gg","http://www.yingtan.gov.cn/xxgk/zfcg/fbgg/index.htm",["name","ggstart_time","href"]],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","yingtan"]

work(conp=conp)