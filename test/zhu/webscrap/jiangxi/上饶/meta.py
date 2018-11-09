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
    locator = (By.XPATH, "/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    cnum = driver.find_element_by_xpath(
        '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[42]/td/div/strong').text.strip()
    url=driver.current_url
    if int(cnum) != num:


        val = driver.find_element_by_xpath(
            "/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[1]/a").text

        main_url = url.rsplit('=',maxsplit=1)[0]
        main_url=main_url+'='+str(num)
        driver.get(main_url)

        locator = (By.XPATH,
                   "/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[1]/a[not(contains(string(),'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    data=[]
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find_all('tr', height=27)
    for tr in trs:
        tds = tr.find_all('td')
        href = tds[0].a['href']
        name = tds[0].a.get_text()
        ggstart_time = tds[1].get_text()
        if 'http' in href:
            href = href
        else:
            href = None

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):

    locator = (By.XPATH, "/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath(
        '//cite').text
    total = re.findall('条/(\d+)页', page)[0]
    total=int(total)
    driver.quit()
    return total

def work(conp,i=-1):
    data=[
        #
        ["gg","http://www.srjsgc.cn/news/list.php?catid=4&page=1",["name","ggstart_time","href"]],
        ["gs","http://www.srjsgc.cn/news/list.php?catid=5&page=1",["name","ggstart_time","href"]],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","shangrao"]

work(conp=conp)