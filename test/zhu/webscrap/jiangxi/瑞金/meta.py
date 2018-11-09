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

#
# url="http://gcjs.gzzbtbzx.com:88/zbgg/more_xian.asp?dq=rj&xian=%C8%F0%BD%F0&keyword=&cut=&page=1"
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
    f1_url=driver.current_url
    if 'gcjs.gzzbtbzx.com:88' in f1_url:
        df=f3(driver,num)
        return df

    locator = (By.XPATH, "/html/body/table[3]/tbody/tr/td[3]/table[2]/tbody/tr[1]/td[2]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    cnum=url.rsplit('=', maxsplit=1)[1]
    # print(cnum)

    if str(num) !=cnum:
        url = url.rsplit('=', maxsplit=1)[0] + '=' + '{}'.format(num)

        val = driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[3]/table[2]/tbody/tr[1]/td[2]/a").text
        driver.get(url)
        locator = (
        By.XPATH, "/html/body/table[3]/tbody/tr/td[3]/table[2]/tbody/tr[1]/td[2]/a[not(contains(string(),'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    url = driver.current_url
    mark = re.findall(r'http://www.rjggzyjyw.com/(.+)\?id=', url)[0]

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    data = []
    trs = soup.find_all('tr', attrs={'bgcolor': '#FFFFFF'})
    for tr in trs:

        tds = tr.find_all('td')
        if mark == 'news_xzgg.asp':
            name = tds[1].get_text().strip()
            href = tds[1].find_all('a')[1]
            href = href['href']
            # print(href)
        else:
            href = tds[1].a['href']

            name = tds[1].a.get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.rjggzyjyw.com/' + href
        ggstart_time = tds[2].get_text()
        click_num = tds[3].get_text()


        tmp = [name, ggstart_time, click_num, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df

def f3(driver,num):
    locator = (By.XPATH, "//td[@bgcolor='#DFDFDF']/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    c_url=driver.current_url
    cnum=re.findall('page=(\d+)',c_url)[0]
    if int(cnum) !=num:
        url = 'http://gcjs.gzzbtbzx.com:88/zbgg/more_xian.asp?dq=rj&xian=%C8%F0%BD%F0&keyword=&cut=&page={}'.format(num)
        val = driver.find_element_by_xpath(
            "//td[@bgcolor='#DFDFDF']/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a").text
        driver.get(url)
        try:
            locator = (By.XPATH,
                       '//td[@bgcolor="#DFDFDF"]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(1)

    main_url = driver.current_url

    data = []
    main_url = main_url.rsplit('/', maxsplit=1)[0]

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find('td', attrs={'bgcolor': '#DFDFDF'})
    table = content.find_all('table')
    table = table[1]
    trss = table.find('table').find('table')
    trs = trss.find_all('tr')

    for i in range(3, len(trs), 2):
        tr = trs[i]
        tds = tr.find_all('td')
        href = tds[0].a['href']
        if 'http' in href:
            href = href
        else:
            href = main_url + '/' + href
        name = tds[0].a.get_text()
        ggstart_time = tds[2].get_text()
        click_num = tds[4].get_text()

        tmp = [name, ggstart_time, click_num, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df

def f2(driver):
    f1_url = driver.current_url
    if 'gcjs.gzzbtbzx.com:88' in f1_url:
        total=109
    else:

        locator = (By.XPATH, "/html/body/table[3]/tbody/tr/td[3]/table[2]/tbody/tr[1]/td[2]/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        try:
            page = driver.find_element_by_xpath(
                "/html/body/table[3]/tbody/tr/td[3]/table[2]/tbody/tr[31]/td/a[2]").get_attribute('href')
            total = page.rsplit('=', maxsplit=1)[1]
        except:
            total=1
    total=int(total)
    driver.quit()
    return total


def work(conp,i=-1):
    data = [
        #
        ["gcjs_zhaobiao_gg", "http://gcjs.gzzbtbzx.com:88/zbgg/more_xian.asp?dq=rj&xian=%C8%F0%BD%F0&keyword=&cut=&page=1",
         ["name", "ggstart_time", "click_num", "href"]],
        # ["gcjs_zhongbiaohx_gg", "http://www.rjggzyjyw.com/more.asp?id=68&city=0&dept=%D6%D0%B1%EA%B9%AB%CA%BE&pageshow=1",
        #  ["name", "ggstart_time", "click_num", "href"]],
        # ["gcjs_dayibucong_gg", "http://www.rjggzyjyw.com/more.asp?id=67&city=0&dept=%B4%F0%D2%C9&pageshow=1",
        #  ["name", "ggstart_time", "click_num", "href"]],
        # #
        # #
        # ["zfcg_zhaobiao_gg", "http://www.rjggzyjyw.com/more.asp?id=57&city=0&dept=%D5%D0%B1%EA%B9%AB%B8%E6&pageshow=1",
        #  ["name", "ggstart_time", "click_num", "href"]],
        # ["zfcg_dayibucong_gg", "http://www.rjggzyjyw.com/more.asp?id=58&city=0&dept=%CF%EE%C4%BF%B4%F0%D2%C9&pageshow=1",
        #  ["name", "ggstart_time", "click_num", "href"]],
        # ["zfcg_zhongbiao_gg", "http://www.rjggzyjyw.com/more.asp?id=59&city=0&dept=%D6%D0%B1%EA%B9%AB%CA%BE&pageshow=1",
        #  ["name", "ggstart_time", "click_num", "href"]],
        #
        #
        # ["xzjy_zhaobiao_gg", "http://www.rjggzyjyw.com/news_xzgg.asp?id=49&ctid=&pageshow=1",["name", "ggstart_time", "click_num", "href"]],
        # ["xzjy_dayibucong_gg", "http://www.rjggzyjyw.com/news_xzgg.asp?id=50&ctid=&pageshow=1",["name", "ggstart_time", "click_num", "href"]],
        # ["xzjy_zhongbiao_gg", "http://www.rjggzyjyw.com/news_xzgg.asp?id=51&ctid=&pageshow=1",["name", "ggstart_time", "click_num", "href"]],

    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","ruijin"]

work(conp=conp)