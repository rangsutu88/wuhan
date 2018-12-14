import pandas as pd  
import re 

from selenium import webdriver 
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

import sys 
import time

import json

from zhulong.util.etl import est_tbs,est_meta,est_html,gg_existed


# driver=webdriver.Chrome()

# url="""http://jyzx.yiyang.gov.cn/jyxx/003001/003001001/2.html"""

# driver.get(url)

_name_='chaohu'

def f1(driver,num):
    url = driver.current_url

    locator = (
    By.XPATH, '/html/body/div[2]/table/tbody/tr/td[3]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum = re.findall('Paging=(\d+)', url)[0]

    main_url = url.rsplit('=', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td[3]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[1]/td[2]/a').text
        url = main_url + '=' + str(num)

        driver.get(url)

        locator = (By.XPATH, '/html/body/div[2]/table/tbody/tr/td[3]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find_all('tr', attrs={'height': 30})

    for tr in trs:
        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a['title']

        ggstart_time = tds[2].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.hfggzy.com' + href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f4(driver,num):
    url = driver.current_url

    locator = (By.XPATH, '//*[@id="form1"]/div[3]/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum = re.findall('Paging=(\d+)', url)[0]

    main_url = url.rsplit('=', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//*[@id="form1"]/div[3]/table/tbody/tr[1]/td[2]/a').text
        url = main_url + '=' + str(num)

        driver.get(url)

        locator = (By.XPATH, '//*[@id="form1"]/div[3]/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('form', id='form1')
    table = div.find('table')
    trs = table.find_all('tr')

    for tr in trs:

        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a['title']

        ggstart_time = tds[2].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.hfggzy.com' + href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df

def f2(driver):
    locator = (
    By.XPATH, '/html/body/div[2]/table/tbody/tr/td[3]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//td[@class="huifont"]').text
        total = re.findall('/(\d+)', page)[0]
        total = int(total)
    except:
        total=1

    driver.quit()
    return total

def f5(driver):

    locator = (By.XPATH, '//*[@id="form1"]/div[3]/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//td[@class="huifont"]').text
        total = re.findall('/(\d+)', page)[0]
        total = int(total)
    except:
        total=1

    driver.quit()
    return total



def f3(driver,url):


    driver.get(url)

    locator=(By.XPATH,'//div[@class="container"]/div/div[2]/table')

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

    div=soup.find('div',class_='container')
    div_1=div.find('div')
    div_2=div_1.find_all('div')[1]
    table=div_2.find('table')
    
    return table



data=[
    #f4#f5
    ["gcjs_zhaobiao_gg","http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003001001&Paging=1",[  'name', 'ggstart_time', 'href','info'],f4,f5],
    ["gcjs_zhongbiaohx_gg","http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003001005&Paging=1",[  'name', 'ggstart_time', 'href','info'],f4,f5],
    ["gcjs_zhongbiao_gg","http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003001003&Paging=1",[  'name', 'ggstart_time', 'href','info'],f4,f5],

    #包含预采和单一性来源
    ["gcjs_gg","http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003001004&Paging=1",[  'name', 'ggstart_time', 'href','info'],f4,f5],

    ["zfcg_zhaobiao_gg","http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003002001&Paging=1",[  'name', 'ggstart_time', 'href','info'],f4,f5],

    #f1#f2
    #包含答疑变更
    ["zfcg_dayibiangeng_gg","http://www.hfggzy.com/chzbtb/jyxx/003002/003002002/?Paging=1",[  'name', 'ggstart_time', 'href','info'],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.hfggzy.com/chzbtb/jyxx/003002/003002003/?Paging=1",[  'name', 'ggstart_time', 'href','info'],f1,f2],

    ["qsy_zhaobiao_gg","http://www.hfggzy.com/chzbtb/jyxx/003004/003004001/?Paging=1",[  'name', 'ggstart_time', 'href','info'],f1,f2],
    ["qsy_dayibiangeng_gg","http://www.hfggzy.com/chzbtb/jyxx/003004/003004002/?Paging=1",[  'name', 'ggstart_time', 'href','info'],f1,f2],
    ["qsy_zhongbiaohx_gg","http://www.hfggzy.com/chzbtb/jyxx/003004/003004003/?Paging=1",[  'name', 'ggstart_time', 'href','info'],f1,f2],
    ["qsy_zhongbiao_gg","http://www.hfggzy.com/chzbtb/jyxx/003004/003004004/?Paging=1",[  'name', 'ggstart_time', 'href','info'],f1,f2],

]



def work(conp,**arg):
    est_meta(conp,data=data,diqu="安徽省巢湖市",**arg)

    est_html(conp,f=f3,**arg)

if __name__=='__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "anhui", "chaohu"])

