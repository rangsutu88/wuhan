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


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
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

    rindex = url.rfind('/')
    main_url = url[:rindex]

    page = driver.page_source
    soup = BeautifulSoup(page, "lxml")
    tables = soup.find('div', class_='ldjs_body')
    lis = tables.find_all('li')
    data = []
    for i in range(0, len(lis), 2):
        li = lis[i]
        href = li.a['href']
        title = li.get_text().strip().strip('•').strip()
        li = lis[i + 1]
        data_time = li.get_text().strip()
        if re.findall('http', href):
            href = href
        else:
            href = main_url + href
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