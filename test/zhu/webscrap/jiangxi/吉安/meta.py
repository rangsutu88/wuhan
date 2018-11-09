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

    locator=(By.XPATH,"//div[@class='pagingList']/ul/li/a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    f1_url=driver.current_url
    mark = re.findall(r'http://www.japrtc.gov.cn/jyxx/(.+?/.+?)/', f1_url)[0]
    # print(mark)
    r_url=f3(mark,num)


    # print(r_url)
    val = driver.find_element_by_xpath("//div[@class='pagingList']/ul/li/a").text
    driver.get(r_url)
    try:
        locator = (By.XPATH, "//div[@class='pagingList']/ul/li/a[not(contains(string(),'%s'))]" % val)
        WebDriverWait(driver, 5).until(locator)
    except:
        time.sleep(1)


    # print('----------------------------------------------',driver.current_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('div', class_='pagingList')
    data = []
    url = driver.current_url
    rindex = url.rfind('/')
    main_url = url[:rindex]
    urs = trs.find_all('li')
    for tr in urs:
        href = tr.a['href'].strip('.')
        name = tr.a.get_text()
        ggstart_time = tr.span.get_text()

        if re.findall('http', href):
            href = href
        else:
            href = main_url + href
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df




def f3(mark,num):
    main_url=''
    list_=[]
    if mark=='jsgc/zbgg':
        # print(mark=='jsgc/zbgg')
        main_url='http://www.japrtc.gov.cn/jyxx/jsgc/zbgg/'
        list_=[50,13,30,34,11,8,6,30,16,30,7,34]
    elif mark=='jsgc/zbgs':
        main_url='http://www.japrtc.gov.cn/jyxx/jsgc/zbgs/'
        list_=[50,7,24,25,7,7,6,12,11,23,3,34]
    elif mark=='jsgc/dyby':
        main_url='http://www.japrtc.gov.cn/jyxx/jsgc/dyby/'
        list_=[50,12,5,9,3,4,5,7,5,5,3,11]
    elif mark=='zfcg/zbgg':
        main_url='http://www.japrtc.gov.cn/jyxx/zfcg/zbgg/'
        list_=[50,12,48,18,24,7,7,15,4,18,6,35]
    elif mark=='zfcg/zbgs':
        main_url='http://www.japrtc.gov.cn/jyxx/zfcg/zbgs/'
        list_=[50,8,13,10,12,6,6,12,4,14,5,23]
    elif mark=='zfcg/dyby':
        main_url='http://www.japrtc.gov.cn/jyxx/zfcg/dyby/'
        list_=[50,3,4,4,3,2,3,4,1,4,2,5]

    if num <= list_[0]:
        if num==1:
            url=main_url+'jas/'
        else:
            url=main_url+'jas/index_{}.htm'.format(num-1)
    elif list_[0] < num <=sum(list_[:2]):
        if num ==list_[0]+1:
            url=main_url+'jax/'
        else:
            url=main_url+'jax/index_{}.htm'.format(num-1-list_[0])
    elif sum(list_[:2]) < num <=sum(list_[:3]):
        if num ==sum(list_[:2])+1:
            url=main_url+'xgx/'
        else:
            url=main_url+'xgx/index_{}.htm'.format(num-1-sum(list_[:2]))
    elif sum(list_[:3]) < num <= sum(list_[:4]):
        if num ==sum(list_[:3])+1:
            url=main_url+'yfx/'
        else:
            url=main_url+'yfx/index_{}.htm'.format(num-1-sum(list_[:3]))
    elif sum(list_[:4]) < num <= sum(list_[:5]):
        if num ==sum(list_[:4])+1:
            url=main_url+'xjx/'
        else:
            url=main_url+'xjx/index_{}.htm'.format(num-1-sum(list_[:4]))
    elif sum(list_[:5]) < num <= sum(list_[:6]):
        if num == sum(list_[:5])+1:
            url=main_url+'jsx/'
        else:
            url=main_url+'jsx/index_{}.htm'.format(num-1-sum(list_[:5]))

    elif sum(list_[:6]) < num <= sum(list_[:7]):
        if num ==sum(list_[:6])+1:
            url=main_url+'thx/'
        else:
            url=main_url+'thx/index_{}.htm'.format(num-1-sum(list_[:6]))
    elif sum(list_[:7]) < num <= sum(list_[:8]):
        if num == sum(list_[:7])+1:
            url=main_url+'wax/'
        else:
            url=main_url+'wax/index_{}.htm'.format(num-1-sum(list_[:7]))
    elif sum(list_[:8]) < num <= sum(list_[:9]):
        if num ==sum(list_[:8])+1:
            url=main_url+'scx/'
        else:
            url=main_url+'scx/index_{}.htm'.format(num-1-sum(list_[:8]))
    elif sum(list_[:9]) < num <= sum(list_[:10]):
        if num ==sum(list_[:9])+1:
            url=main_url+'afx/'
        else:
            url=main_url+'afx/index_{}.htm'.format(num-1-sum(list_[:9]))
    elif sum(list_[:10]) < num <= sum(list_[:11]):
        if num ==sum(list_[:10])+1:
            url=main_url+'yxx/'
        else:
            url=main_url+'yxx/index_{}.htm'.format(num-1-sum(list_[:10]))
    elif sum(list_[:11]) < num <= sum(list_[:12]):
        if num ==sum(list_[:11])+1:
            url=main_url+'jgss/'
        else:
            url=main_url+'jgss/index_{}.htm'.format(num-1-sum(list_[:11]))

    r_url=url
    return r_url

def f2(driver):

    locator = (By.XPATH, "//div[@class='pagingList']/ul/li/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    total = 0
    for i in range(1,13):

        val = driver.find_element_by_xpath("//div[@class='pagingList']/ul/li/a").text
        driver.find_element_by_xpath("//div[@class='pagingTitle-list']/ul/li[{num}]/a".format(num=i)).click()
        try:
            locator = (By.XPATH, "//div[@class='pagingList']/ul/li/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver,10).until(locator)
        except:
            time.sleep(1)
        try:
            page = driver.find_element_by_xpath('//*[@id="div_page"]/a[last()]').get_attribute('href')
            total_ = re.findall(r'index_(\d+).htm', page)[0]
        except:
            total_=0

        total = total + int(total_) + 1
    return total

def work(conp,i=-1):
    data=[
        #
        ["gcjs_zhaobiao_gg","http://www.japrtc.gov.cn/jyxx/jsgc/zbgg/",["name","ggstart_time","href"]],
        ["gcjs_zhongbiaohx_gg","http://www.japrtc.gov.cn/jyxx/jsgc/zbgs/",["name","ggstart_time","href"]],
        ["gcjs_dayibucong_gg","http://www.japrtc.gov.cn/jyxx/jsgc/dyby/",["name","ggstart_time","href"]],


        ["zfcg_zhaobiao_gg","http://www.japrtc.gov.cn/jyxx/zfcg/zbgg/",["name","ggstart_time","href"]],
        ["zfcg_dayibucong_gg","http://www.japrtc.gov.cn/jyxx/zfcg/dyby/",["name","ggstart_time","href"]],
        ["zfcg_zhongbiao_gg","http://www.japrtc.gov.cn/jyxx/zfcg/zbgs/",["name","ggstart_time","href"]],

    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","jian"]

work(conp=conp)