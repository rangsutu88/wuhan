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

    locator = (By.XPATH, '//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    cnum = re.findall('-(\d+?)\.html', url)[0]

    main_url = url.rsplit('-', maxsplit=1)[0]

    if int(cnum) != num:
        main_url=main_url+'-'+str(num)+'.html'
        val = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span').text

        driver.get(main_url)

        locator = (By.XPATH, '//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data=[]
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_='lb_ul')
    lis = div.find_all('li')
    for li in lis:
        href = li.a['href']
        name = li.a.span.get_text()
        ggstart_time = li.find('span', class_='sp2').get_text()

        if 'http' in href:
            href = href
        else:
            href = None

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):

    locator = (By.XPATH, '//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[3]/div[2]/a[4]').get_attribute('href')

    total = re.findall('-(\d+?)\.html', page)[0]
    total=int(total)
    driver.quit()
    return total

def work(conp,i=-1):
    data=[
        #
        ["zfcg_gg","http://www.dxs.gov.cn/news-list-zfcg-1.html",["name","ggstart_time","href"]],

    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","dexing"]

work(conp=conp)