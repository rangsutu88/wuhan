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
from zhulong.util.etl import gg_meta,gg_html



# driver=webdriver.Chrome()

# url="""http://jyzx.yiyang.gov.cn/jyxx/003001/003001001/2.html"""

# driver.get(url)


def f1(driver,num):

    locator = (By.XPATH, '//ul[@class="wb-data-item"]/li/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    main_url = url.rsplit('/', maxsplit=1)[0]
    if 'project' in url:
        cnum=1
    else:
        cnum=re.findall(r'/(\d+)\.html',url)[0]

    if cnum != str(num):
        if num == 1:
            url=main_url+'/project.html'
        else:
            url=main_url + '/' + str(num) + '.html'
        val = driver.find_element_by_xpath('//ul[@class="wb-data-item"]/li[1]/div/a').text
        driver.get(url)

        # 第二个等待
        locator = (By.XPATH, '//*[@id="jt"]/ul/li[1]/div/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('ul', class_='wb-data-item')
    lis = div.find_all('li')

    for tr in lis:

        div = tr.find('div')
        href = div.a['href']
        content = div.a['title']
        ggstart_time = tr.find('span', recursive=False).get_text()
        if 'http' in href:
            href = href
        else:
            href = 'http://www.aqzbcg.org:1102' + href
        tmp = [content, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"]=None
    return df 


def f2(driver):
    locator = (By.XPATH, '//ul[@class="wb-data-item"]/li/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//li[@class="wb-page-li"][1]/span').text
    total = re.findall('/(\d+)', page)[0]
    total = int(total)

    driver.quit()
    return total


def f3(driver,url):

    driver.get(url)

    locator = (By.CLASS_NAME, 'ewb-con')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    div = soup.find('div', class_='ewb-con')
    
    return div


data=[
["gcjs_zhaobiao_gg","http://www.aqzbcg.org:1102/jyxx/012001/012001001/project.html",["name","ggstart_time","href","info"],f1,f2],
["gcjs_dayibiangeng_gg","http://www.aqzbcg.org:1102/jyxx/012001/012001002/project.html",["name","ggstart_time","href","info"],f1,f2],
["gcjs_zhongbiaohx_gg","http://www.aqzbcg.org:1102/jyxx/012001/012001003/project.html",["name","ggstart_time","href","info"],f1,f2],
["gcjs_zhongbiao_gg","http://www.aqzbcg.org:1102/jyxx/012001/012001004/project.html",["name","ggstart_time","href","info"],f1,f2],

["zfcg_zhaobiao_gg","http://www.aqzbcg.org:1102/jyxx/012002/012002001/project.html",["name","ggstart_time","href","info"],f1,f2],
["zfcg_dayibiangeng_gg","http://www.aqzbcg.org:1102/jyxx/012002/012002002/project.html",["name","ggstart_time","href","info"],f1,f2],
#包含流标中标
["zfcg_zhong_gg","http://www.aqzbcg.org:1102/jyxx/012002/012002003/project.html",["name","ggstart_time","href","info"],f1,f2],

["chouqian_zhaobiao_gg","http://www.aqzbcg.org:1102/jyxx/012005/012005001/project.html",["name","ggstart_time","href","info"],f1,f2],
["chouqian_dayibiangeng_gg","http://www.aqzbcg.org:1102/jyxx/012005/012005002/project.html",["name","ggstart_time","href","info"],f1,f2],
["chouqian_zhongbiao_gg","http://www.aqzbcg.org:1102/jyxx/012005/012005003/project.html",["name","ggstart_time","href","info"],f1,f2],

]

def work(conp):
    gg_meta(conp,data=data,diqu="安徽省安庆市")

    gg_html(conp,f=f3)


work(conp=["postgres","since2015","192.168.3.171","anhui","anqing"])

