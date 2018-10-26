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
    "num":10,
    # 'total':2


    }
    m=web()
    m.write(**setting)


def f1(driver,num):
    locator=(By.XPATH,'//*[@id="main"]/div[1]/ul/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    cnum=url.rsplit('-',maxsplit=1)[1]
    if str(num) !=cnum:
        url = url.rsplit('-', maxsplit=1)[0] + '-' + str(num)
        val=driver.find_element_by_xpath('//*[@id="main"]/div[1]/ul/li[1]/a').text
        driver.get(url)
        locator=(By.XPATH,"//*[@id='main']/div[1]/ul/li[1]/a[not(contains(string(),'%s'))]"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    uls = soup.find('ul', class_='list')
    data = []
    url = driver.current_url
    rindex = url.rfind('/')
    main_url = url[:rindex]
    lis = uls.find_all('li')

    for li in lis:
        href = li.a['href']
        href = 'http://www.lssggzy.gov.cn' + href
        name = li.a.get_text().strip()
        ggstart_time = li.span.get_text()

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):
    url=driver.current_url
    if url=='http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-45-1':
        total=22
    elif url=='http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-48-1':
        total=81
    elif url=='http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-49-1':
        total=54
    elif url=='http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-52-1':
        total=86
    else:
        total=1
    driver.quit()
    return total

def work(conp,i=-1):
    data=[
        #
        ["gcjs_zhaobiao_gg","http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-45-1",["name","ggstart_time","href"]],
        ["gcjs_zhongbiaohx_gg","http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-48-1",["name","ggstart_time","href"]],

        ["zfcg_zhaobiao_gg","http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-49-1",["name","ggstart_time","href"]],
        ["zfcg_zhongbiao_gg","http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-52-1",["name","ggstart_time","href"]],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","lushan"]

work(conp=conp)