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


from zhulong.util.etl import est_tbs,est_meta,est_html
# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



def f1(driver,num):
    locator=(By.XPATH,'//*[@id="comp_5790085"]/div/ul[1]/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    if "index.html" in url:
        cnum=1
    else:
        cnum=int(re.findall("index_([0-9]{1,}).html",url)[0])+1
    if num!=cnum:
        if num==1:
            url=re.sub("index[_0-9]*.html","index.html",url)
        else:
            s="index_%d.html"%(num-1) if num>1 else "index.html"
            url=re.sub("index[_0-9]*.html",s,url)

        val = driver.find_element_by_xpath('//*[@id="comp_5790085"]/div/ul[1]/li[1]/a').text
        driver.get(url)
        locator = (By.XPATH, "//*[@id='comp_5790085']/div/ul[1]/li[1]/a[not(contains(string(),'%s'))]" % val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    main_url = driver.current_url
    main_url = main_url.rsplit('/', maxsplit=1)[0]
    data=[]
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_='clist_con')
    lis = div.find_all('li')
    for li in lis:
        href = li.a['href'].strip('.')
        if 'http' in href:
            href = href
        else:
            href = main_url + href
        name = li.a.get_text().strip()
        ggstart_time = li.span.a.get_text()
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, "//tr[@class='tdLine'][1]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//a[@class="clz1"][last()]').get_attribute('href')
    total = re.findall(r'index_(\d+).htm', page)[0]
    total=int(total)+1
    return total


data=[
    # 数据量太少，未爬取
    # ["gcjs_zhaobiao_gg","http://www.jjjsj.gov.cn/csjs/jzgc/index_1.html",["name","ggstart_time","href"]],
    # ["gcjs_shizheng_zhaobiao_gg","http://www.jjjsj.gov.cn/csjs/szyl/index_1.html",["name","ggstart_time","href"]],
]
def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省九江市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    conp=["testor","zhulong","192.168.3.171","test","lch"]
    # conp=["testor","zhulong","192.168.3.171","test","public"]
    # conp=["postgres","since2015","192.168.3.171","jiangxi","jiujiang"]

    work(conp=conp)