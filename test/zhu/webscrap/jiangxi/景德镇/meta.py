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
    locator = (By.XPATH, '//*[@id="rightout"]/div[1]/ul/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    cnum=url.rsplit('/', maxsplit=1)[1].split('.')[0]


    if str(num) !=cnum:
        url = url.rsplit('/', maxsplit=1)[0] + '/' + '{}.html'.format(num)

        val = driver.find_element_by_xpath('//*[@id="rightout"]/div[1]/ul/li[1]/a').text
        driver.get(url)
        locator = (By.XPATH, "//*[@id='rightout']/div[1]/ul/li[1]/a[not(contains(string(),'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    data = []
    uls = soup.find('div', class_='menu-list')
    lis = uls.find_all('li')
    for li in lis:
        # print(li)
        href = li.a['href'].strip('.')
        name = li.a.get_text().strip()
        ggstart_time = li.span.get_text().strip()
        if 'http' in href:
            href = href
        else:
            href = 'http://www.jdz.gov.cn' + href


        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):
    locator = (By.XPATH, '//*[@id="rightout"]/div[1]/ul/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//*[@id="index"]').text
    total = int(page.strip().split('/')[1])
    driver.quit()
    return total

def work(conp,i=-1):
    data=[
        #
        ["gcjs_zhaobiao_gg","http://www.jdz.gov.cn/xxgk/050014/050014004/1.html",["name","ggstart_time","href"]],
        ["gcjs_zhongbiao_gg","http://www.jdz.gov.cn/xxgk/050014/050014005/1.html",["name","ggstart_time","href"]],
        ["zfcg_gg","http://www.jdz.gov.cn/xxgk/050014/050014003/1.html",["name","ggstart_time","href"]],



    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","jingdezhen"]

work(conp=conp)