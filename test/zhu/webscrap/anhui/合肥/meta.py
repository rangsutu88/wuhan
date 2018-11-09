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


url="http://ggzy.hefei.gov.cn/jyxx/002001/002001002/moreinfo_jyxx.html"
driver=webdriver.Chrome()
driver.minimize_window()
driver.get(url)
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


def f4(driver,num):
    url=driver.current_url
    locator = (By.XPATH, '//*[@id="container"]/div[3]/div/div/div[2]/div[2]/ul/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    if 'moreinfo' in url:
        cnum=1
    else:
        cnum = re.findall('\/(\d+?).html', url)[0]

    main_url = url.rsplit('/', maxsplit=1)[0]
    if int(cnum) != num:
        val = driver.find_element_by_xpath('//*[@id="container"]/div[3]/div/div/div[2]/div[2]/ul/li[1]/a').text
        url = main_url + '/' + str(num) + '.html'

        driver.get(url)

        locator = (By.XPATH, '//*[@id="container"]/div[3]/div/div/div[2]/div[2]/ul/li[1]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    ul=soup.find('ul',class_='ewb-list')
    lis=ul.find_all('li')
    for li in lis:
        address = li.find('span', class_='ewb-label1 l').get_text().strip('】').strip('【')
        href = li.a['href'].strip('.')
        name = li.a.get_text()
        ggstart_time = li.find('span', class_='ewb-list-date r').get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.hefei.gov.cn' + href

        tmp = [address, name, ggstart_time, href]
        print(tmp)
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df


def f1(driver,num):
    url = driver.current_url
    if 'gggs' in url:
        df=f4(driver,num)
        return df

    locator = (By.XPATH, '/html/body/ul/li[1]/a/span[3]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    if 'moreinfo' in url:
        cnum=1
    else:
        cnum = re.findall('\/(\d+?).html', url)[0]

    main_url = url.rsplit('/', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('/html/body/ul/li[1]/a/span[3]').text
        url = main_url + '/' + str(num) + '.html'

        driver.get(url)

        locator = (By.XPATH, '/html/body/ul/li[1]/a/span[3][not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('ul', class_='ewb-right-item')
    lis = div.find_all('li')
    for li in lis:
        address = li.find('span', class_='ewb-label1 l').get_text().strip('】').strip('【')

        href = li.a['href'].strip('.')
        name = li.find('span', class_='ewb-context l').get_text()
        ggstart_time = li.find('span', recursive=False).get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.hefei.gov.cn' + href


        tmp = [address, name, ggstart_time, href]
        print(tmp)
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):
    url = driver.current_url
    if 'gggs' in url:
        locator = (By.XPATH, '//*[@id="container"]/div[3]/div/div/div[2]/div[2]/ul/li[1]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    else:
        locator = (By.XPATH, '/html/body/ul/li[1]/a/span[3]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    try:

        page = driver.find_element_by_xpath('//*[@id="index"]').text
        total = re.findall('/(\d+)', page)[0]
        total = int(total)
    except:
        total=1

    driver.quit()
    return total

def work(conp,i=-1):
    data=[
        #
        ["gcjs_zhaobiao_gg","http://ggzy.hefei.gov.cn/jyxx/002001/002001001/moreinfo_jyxxgg.html",['address', 'status', 'name', 'ggstart_time', 'href']],
        ["gcjs_chengqingbiangeng_gg","http://ggzy.hefei.gov.cn/jyxx/002001/002001002/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href']],
        ["gcjs_zhongbiaohx_gg","http://ggzy.hefei.gov.cn/jyxx/002001/002001003/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href']],
        ["gcjs_zhongbiao_gg","http://ggzy.hefei.gov.cn/jyxx/002001/002001004/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href']],

        ["zfcg_zhaobiao_gg","http://ggzy.hefei.gov.cn/jyxx/002002/002002001/moreinfo_jyxxgg.html",['address', 'status', 'name', 'ggstart_time', 'href']],
        ["zfcg_dayibiangeng_gg","http://ggzy.hefei.gov.cn/jyxx/002002/002002002/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href']],
        ["zfcg_zhongbiao_gg","http://ggzy.hefei.gov.cn/jyxx/002002/002002004/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href']],

        ["qsy_zhaobiao_gg","http://ggzy.hefei.gov.cn/jyxx/002008/002008001/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href']],
        ["qsy_biangen_gg","http://ggzy.hefei.gov.cn/jyxx/002008/002008002/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href']],
        ["qsy_jieguo_gg","http://ggzy.hefei.gov.cn/jyxx/002008/002008003/moreinfo_jyxx.html",['address',  'name', 'ggstart_time', 'href']],

        ["qsy_dyxly_gg","http://ggzy.hefei.gov.cn/gggs/003003/moreinfo2.html",['address',  'name', 'ggstart_time', 'href']],
        ["qsy_yvcai_gg","http://ggzy.hefei.gov.cn/gggs/003002/moreinfo2.html",['address',  'name', 'ggstart_time', 'href']],

    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["postgres","since2015","192.168.3.171","anhui","hefei"]

# work(conp=conp)