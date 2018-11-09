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



def f1(driver,num):
    try:
        locator = (By.XPATH, '//*[@id="gengerlist"]/div[1]/ul/li[1]/a')
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
    except:
        title = driver.title
        if title == '404 Not Found':
            data = []
            tmp = [None, None, None]
            data.append(tmp)
            df = pd.DataFrame(data=data)
            return df
        else:
            locator = (By.XPATH, '//*[@id="gengerlist"]/div[1]/ul/li[1]/a')
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    cnum=int(re.findall("/([0-9]{1,}).html",url)[0])

    if num!=cnum:
        s="/%d.html"%(num)
        url=re.sub("/[0-9]{1,}.html",s,url)
        val=driver.find_element_by_xpath('//*[@id="gengerlist"]/div[1]/ul/li[1]/a').text

        driver.get(url)

        try:
            locator=(By.XPATH,"//*[@id='gengerlist']/div[1]/ul/li[1]/a[not(contains(string(),'%s'))]"%val)
            WebDriverWait(driver,5).until(EC.presence_of_element_located(locator))
        except:
            title = driver.title
            if title == '404 Not Found':
                data = []
                tmp = [None, None, None]
                data.append(tmp)
                df = pd.DataFrame(data=data)
                return df
            else:
                locator = (By.XPATH, "//*[@id='gengerlist']/div[1]/ul/li[1]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
    ht = driver.page_source
    soup = BeautifulSoup(ht, 'lxml')
    uls = soup.find('div', class_="ewb-infolist")
    lis = uls.find_all('li')
    data=[]
    for li in lis:
        title = li.a.get_text()
        href = li.a['href']
        href = 'http://www.jxsggzy.cn' + href
        date_time = li.span.get_text()
        tmp = [title, date_time,href]
        data.append(tmp)
    df=pd.DataFrame(data=data)

    return df


def f2(driver):

    locator = (By.XPATH, '//*[@id="gengerlist"]/div[1]/ul/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    try:
        total=int(driver.find_element_by_xpath('//*[@id="index"]').text.split('/')[1])
    except:
        total=1

    driver.quit()
    return total

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
    # "total":10


    }
    m=web()
    m.write(**setting)


def work(conp,i=-1):
    data=[

        # ["gcjs_fangwushizheng_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002001/002001001/1.html",["name","ggstart_time","href"]],
        # ["gcjs_fangwushizheng_dayi_gg","http://www.jxsggzy.cn/web/jyxx/002001/002001002/1.html",["name","ggstart_time","href"]],
        # ["gcjs_fangwushizheng_zhongbiaohx_gg","http://www.jxsggzy.cn/web/jyxx/002001/002001004/1.html",["name","ggstart_time","href"]],

        # ["gcjs_jiaotong_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002002/002002002/1.html",["name","ggstart_time","href"]],
        # ["gcjs_jiaotong_buyi_gg","http://www.jxsggzy.cn/web/jyxx/002002/002002003/1.html",["name","ggstart_time","href"]],
        # ["gcjs_jiaotong_zhongbiaohx_gg","http://www.jxsggzy.cn/web/jyxx/002002/002002005/1.html",["name","ggstart_time","href"]],

        # ["gcjs_shuili_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002003/002003001/1.html",["name","ggstart_time","href"]],
        # ["gcjs_shuili_dayi_gg","http://www.jxsggzy.cn/web/jyxx/002003/002003002/1.html",["name","ggstart_time","href"]],
        # ["gcjs_shuili_zhongbiaohx_gg","http://www.jxsggzy.cn/web/jyxx/002003/002003004/1.html",["name","ggstart_time","href"]],

        # ["gcjs_zhongdian_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002005/002005001/1.html",["name","ggstart_time","href"]],
        # ["gcjs_zhongdian_dayi_gg","http://www.jxsggzy.cn/web/jyxx/002005/002005002/1.html",["name","ggstart_time","href"]],
        # ["gcjs_zhongdian_zhongbiaohx_gg","http://www.jxsggzy.cn/web/jyxx/002005/002005004/1.html",["name","ggstart_time","href"]],

        # ["zfcg_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002006/002006001/1.html",["name","ggstart_time","href"]],
        # ["zfcg_biangeng_gg","http://www.jxsggzy.cn/web/jyxx/002006/002006002/1.html",["name","ggstart_time","href"]],
        # ["zfcg_dayi_gg","http://www.jxsggzy.cn/web/jyxx/002006/002006003/1.html",["name","ggstart_time","href"]],
        # ["zfcg_zhongbiao_gg","http://www.jxsggzy.cn/web/jyxx/002006/002006004/1.html",["name","ggstart_time","href"]],

        # ["yycg_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002010/002010001/1.html",["name","ggstart_time","href"]],
        # ["yycg_zhongbiao_gg","http://www.jxsggzy.cn/web/jyxx/002010/002010002/1.html",["name","ggstart_time","href"]],

        # ["qita_zhaobiao_gg","http://www.jxsggzy.cn/web/jyxx/002013/002013001/1.html",["name","ggstart_time","href"]],
        # ["qita_zhongbiao_gg","http://www.jxsggzy.cn/web/jyxx/002013/002013002/1.html",["name","ggstart_time","href"]]

        #以下需要在数据库中手动合并为zfcg_zhaobiao_gg

        ["zfcg_dyxly_gg","http://www.jxsggzy.cn/web/jyxx/002006/002006005/1.html",["name","ggstart_time","href"]]


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","jiangxi"]

work(conp=conp)