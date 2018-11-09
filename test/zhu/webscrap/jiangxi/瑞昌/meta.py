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
    "num":5,
    # 'total':5


    }
    m=web()
    m.write(**setting)


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
    # print(len(trs))
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
        #
        # tmp = [index_num]
        tmp = [index_num, status, gksj, gkfw, name,  ggstart_time,href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):
    locator = (
    By.XPATH, '/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[3]/tbody/tr[2]/td[1]/div')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath(
        '/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[5]/tbody/tr/td/div').text

    total = re.findall('总共(\d+?)页', page)[0]
    total=int(total)
    return total

def work(conp,i=-1):
    data=[

        # ["zfcg_gg","http://218.65.3.188/rcs/cjxx/zfcgyztb/index.htm",['index_num','type','gksj','gkfw',"name","ggstart_time","href"]],
        ["gcjs_gg","http://218.65.3.188/rcs/gddt/gggs/index.htm",['index_num','type','gksj','gkfw',"name","ggstart_time","href"]],

    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","ruichang"]

work(conp=conp)