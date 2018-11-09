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


# url="http://ggzy.hefei.gov.cn/jyxx/002001/002001002/moreinfo_jyxx.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
def general_template(tb,url,col,f1,f2,conp):

    m=web()
    setting={
    "url":url,
    "f1":f1,
    "f2":f2,
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":1,
    'total':2


    }
    m=web()
    m.write(**setting)


def f3(driver,num):
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
        try:
            status = tds[1].font.get_text().strip('[').strip(']')
        except Exception as e:
            status = 0

        ggstart_time = tds[2].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.hfggzy.com' + href

        tmp = [name, status, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df

def f6(driver):
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



def work(conp,i=-1):
    data=[
        #f4#f5
        ["gcjs_zhaobiao_gg","http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003001001&Paging=1",[  'name','status', 'ggstart_time', 'href'],f4,f5],
        ["gcjs_zhongbiaohx_gg","http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003001005&Paging=1",[  'name','status', 'ggstart_time', 'href'],f4,f5],
        ["gcjs_zhongbiao_gg","http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003001003&Paging=1",[  'name','status', 'ggstart_time', 'href'],f4,f5],
        ["gcjs_biaoqian_gg","http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003001004&Paging=1",[  'name','status', 'ggstart_time', 'href'],f4,f5],

        ["zfcg_zhaobiao_gg","http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003002001&Paging=1",[  'name','status', 'ggstart_time', 'href'],f4,f5],


        #f3#f6
        ["zfcg_dayibiangeng_gg","http://www.hfggzy.com/chzbtb/jyxx/003002/003002002/?Paging=1",[  'name', 'ggstart_time', 'href'],f3,f6],
        ["zfcg_zhongbiao_gg","http://www.hfggzy.com/chzbtb/jyxx/003002/003002003/?Paging=1",[  'name', 'ggstart_time', 'href'],f3,f6],

        ["chouqian_zhaobiao_gg","http://www.hfggzy.com/chzbtb/jyxx/003004/003004001/?Paging=1",[  'name', 'ggstart_time', 'href'],f3,f6],
        ["chouqian_dayibiangeng_gg","http://www.hfggzy.com/chzbtb/jyxx/003004/003004002/?Paging=1",[  'name', 'ggstart_time', 'href'],f3,f6],
        ["chouqian_zhongbiaohx_gg","http://www.hfggzy.com/chzbtb/jyxx/003004/003004003/?Paging=1",[  'name', 'ggstart_time', 'href'],f3,f6],
        ["chouqian_zhongbiao_gg","http://www.hfggzy.com/chzbtb/jyxx/003004/003004004/?Paging=1",[  'name', 'ggstart_time', 'href'],f3,f6],

    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],w[3],w[4],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","anhui","chaohu"]

work(conp=conp)