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
        # 'total':5


    }
    m=web()
    m.write(**setting)


def f1(driver,num):
    locator=(By.XPATH,"//table[@class='bg'][1]/tbody/tr/td/a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    mark = re.findall('/((\w+?)/(\w+?))/index', url)[0][0]
    if mark=='zbgs/gkzb':
        if num <=17:
            if "index.htm" in url:
                cnum = 1
            else:
                cnum = int(re.findall("index_([0-9]{1,}).htm", url)[0]) + 1
            if num != cnum:
                if num == 1:
                    url = re.sub("index[_0-9]*.htm", "index.htm", url)
                else:
                    s = "index_%d.htm" % (num - 1) if num > 1 else "index.htm"
                    url = re.sub("index[_0-9]*.htm", s, url)
                val = driver.find_element_by_xpath("//table[@class='bg'][1]/tbody/tr/td/a").text
                driver.get(url)
                locator = (By.XPATH, "//table[@class='bg'][1]/tbody/tr/td/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        elif num > 17:
            num=num-17
            url='http://www.fzztb.gov.cn/jsgc/zbgs/yqzb/index.htm'

            if num == 1:
                url = 'http://www.fzztb.gov.cn/jsgc/zbgs/yqzb/index.htm'
            else:
                s = "index_%d.htm" % (num - 1) if num > 1 else "index.htm"
                url = re.sub("index.htm", s, url)
            val = driver.find_element_by_xpath("//table[@class='bg'][1]/tbody/tr/td/a").text
            driver.get(url)
            locator = (By.XPATH, "//table[@class='bg'][1]/tbody/tr/td/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    elif mark == 'zbgs/yqzb':
        num=num-17

        if "index.htm" in url:
            cnum = 1
        else:
            cnum = int(re.findall("index_([0-9]{1,}).htm", url)[0]) + 1
        if num != cnum:
            if num == 1:
                url = re.sub("index[_0-9]*.htm", "index.htm", url)
            else:
                s = "index_%d.htm" % (num - 1) if num > 1 else "index.htm"
                url = re.sub("index[_0-9]*.htm", s, url)
            val = driver.find_element_by_xpath("//table[@class='bg'][1]/tbody/tr/td/a").text
            driver.get(url)
            locator = (By.XPATH, "//table[@class='bg'][1]/tbody/tr/td/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    else:
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
            val=driver.find_element_by_xpath("//table[@class='bg'][1]/tbody/tr/td/a").text
            driver.get(url)
            locator=(By.XPATH,"//table[@class='bg'][1]/tbody/tr/td/a[not(contains(string(),'%s'))]"%val)
            WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))


    rindex = url.rfind('/')
    main_url = url[:rindex]

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    data=[]
    tables = soup.find_all('table', class_='bg')
    for table in tables:
        tds = table.find_all('td')
        name = tds[0].a['title']
        href = tds[0].a['href']
        ggstart_time = tds[1].get_text()

        if re.findall('http', href):
            href = href
        elif re.findall('\.\.\/\.\.',href):

            href = 'http://www.fzztb.gov.cn/'+href.strip(r'../..')

        else:
            href=main_url+href.strip(r'.')

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):
    locator = (By.XPATH, "//table[@class='bg'][1]/tbody/tr/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    if url=='http://www.fzztb.gov.cn/jsgc/zbgs/gkzb/index.htm':
        page = driver.find_element_by_xpath("(//*[@class='cy05'])[last()]").get_attribute('href')
        total = re.findall(r'index_(\d+).htm', page)[0]
        total_1 = int(total) + 1
        val=driver.find_element_by_xpath("//table[@class='bg'][1]/tbody/tr/td/a").text
        driver.get('http://www.fzztb.gov.cn/jsgc/zbgs/yqzb/index.htm')
        locator = (By.XPATH, "//table[@class='bg'][1]/tbody/tr/td/a[not(contains(string(),'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        page_2=driver.find_element_by_xpath("(//*[@class='cy05'])[last()]").get_attribute('href')
        total = re.findall(r'index_(\d+).htm', page_2)[0]
        total_2 = int(total) + 1
        total=total_1+total_2
    else:
        page = driver.find_element_by_xpath("(//*[@class='cy05'])[last()]").get_attribute('href')
        total = 0 if re.findall(r'index_(\d+).htm', page) ==[] else re.findall(r'index_(\d+).htm', page)[0]
        total=int(total)+1

    return total

def work(conp,i=-1):
    data=[

        ["gcjs_zhaobiao_gg","http://www.fzztb.gov.cn/jsgc/zbgg/index.htm",["name","ggstart_time","href"]],
        ["gcjs_zhongbiaohx_gg","http://www.fzztb.gov.cn/jsgc/zbgs/gkzb/index.htm",["name","ggstart_time","href"]],
        ["gcjs_liubiao_gg","http://www.fzztb.gov.cn/jsgc/lbgs/index.htm",["name","ggstart_time","href"]],
        ["gcjs_xianjixingxi_gg","http://www.fzztb.gov.cn/jsgc/xjxx/index.htm",["name","ggstart_time","href"]],


        ["zfcg_zhaobiao_gg","http://www.fzztb.gov.cn/zfcg/zbgg/gkzb/index.htm",["name","ggstart_time","href"]],
        ["zfcg_xianjixingxi_gg","http://www.fzztb.gov.cn/zfcg/xjxx/index.htm",["name","ggstart_time","href"]],
        ["zfcg_liubiao_gg","http://www.fzztb.gov.cn/zfcg/lbgs/index.htm",["name","ggstart_time","href"]],
        ["zfcg_zhongbiao_gg","http://www.fzztb.gov.cn/zfcg/zbgs/index.htm",["name","ggstart_time","href"]],
        ["zfcg_tanpan_gg","http://www.fzztb.gov.cn/zfcg/zbgg/jzxtp/index.htm",["name","ggstart_time","href"]],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["postgres","since2015","192.168.3.171","jiangxi","fuzhou"]

work(conp=conp)