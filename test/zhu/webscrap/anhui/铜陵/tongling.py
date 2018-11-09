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
    url = driver.current_url

    locator = (By.XPATH, '//*[@id="DataGrid1"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum = re.findall('Paging=(\d+)', url)[0]

    main_url = url.rsplit('=', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//*[@id="DataGrid1"]/tbody/tr[1]/td[2]/a').text
        url = main_url + '=' + str(num)

        driver.get(url)
        locator = (By.XPATH, '//*[@id="DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('table', id='DataGrid1')
    trs = div.find_all('tr')

    for tr in trs:

        tds = tr.find_all('td')
        href = tds[1].a['href']
        content = tds[1].a.get_text().strip()
        # print(content)
        try:
            name = re.findall('(.+)\[', content)[0]
        except:
            name = content

        ggstart_time = tds[2].span.get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.tlzbcg.com' + href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"]=None
    return df 

def f4(driver,num):
    url = driver.current_url

    locator = (By.XPATH, '//table[@class="moreinfocon"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum = re.findall('Paging=(\d+)', url)[0]

    main_url = url.rsplit('=', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//table[@class="moreinfocon"]/tbody/tr[1]/td[2]/a').text
        url = main_url + '=' + str(num)

        driver.get(url)
        locator = (By.XPATH, '//table[@class="moreinfocon"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('table', class_='moreinfocon')
    trs = div.find_all('tr')

    for tr in trs:

        tds = tr.find_all('td')
        href = tds[1].a['href']
        content = tds[1].a['title']
        # print(content)
        try:
            name = re.findall('(.+)\[', content)[0]
        except:
            name = content

        ggstart_time = tds[2].span.get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.tlzbcg.com' + href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df

def f5(driver,num):
    url = driver.current_url
    locator = (By.XPATH, '//ul[@class="mored"]/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum = re.findall('Paging=(\d+)', url)[0]

    main_url = url.rsplit('=', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//ul[@class="mored"]/li[1]/div/a').text
        url = main_url + '=' + str(num)
        driver.get(url)
        locator = (By.XPATH, '//ul[@class="mored"]/li[1]/div/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('ul', class_='mored')
    trs = div.find_all('li')

    for li in trs:
        ggstart_time = li.i.get_text()
        ggstart_time = re.findall('\[(.+\])', ggstart_time)[0]
        href = li.div.a['href']
        name = li.div.a['title']

        if 'http' in href:
            href = href
        else:
            if 'zyx' in url:
                href = 'http://zyx.tlzbcg.com' + href
            elif 'yaq' in url:
                href = 'http://yaq.tlzbcg.com' + href
            else:
                href=href
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df



def f2(driver):
    locator = (By.XPATH,
       '//*[@id="DataGrid1"]/tbody/tr[1]/td[2]/a | '
       '//table[@class="moreinfocon"]/tbody/tr[1]/td[2]/a |'
       ' //ul[@class="mored"]/li[1]/div/a')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//div[@class="pageText xxxsHidden"][1] | //td[@class="huifont"]').text
        total = re.findall('/(\d+)', page)[0]
        total = int(total)
    except:
        total = 1

    driver.quit()
    return total




def f3(driver,url):
    driver.get(url)
    locator = (
    By.XPATH, '//*[@id="tblInfo"] | //div[@id="menutab_6_1"]/.. | //div[@class="container clearfix"]')

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

    if 'tlsggzy' in url:
        try:
            div = soup.find('div', class_="container clearfix").find('table').find_all('tr')[2]
        except:
            div = soup.find('div', attrs={'id': re.compile('menutab_6_\d'), 'style': ''})

    elif  'yaq' in url:
        div = soup.find('td', class_="infodetail") #枞阳县、义安区
    elif 'zyx' in url:
        div = soup.find('td', class_="infodetail")  # 枞阳县、义安区
    else:
        div = soup.find('div', class_="container clearfix").find('table').find_all('tr')[2]


    
    return div


data = [
    #
    # ["gcjs_zhaobiao_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001001&Paging=1",['name', 'ggstart_time', 'href',"info"],f1,f2],
    # ["gcjs_zhongbiaohx_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001003&Paging=1", ['name', 'ggstart_time', 'href',"info"],f1,f2],
    # ["gcjs_zhongbiao_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001004&Paging=1",  ['name',  'ggstart_time', 'href',"info"],f1,f2],
    # ["gcjs_liubiao_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001006&Paging=1",['name',  'ggstart_time', 'href',"info"],f1,f2],
    #
    # ["gcjs_dingdianchouqian_zhaobiao_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006002001&Paging=1",['name',  'ggstart_time', 'href',"info"],f1,f2],
    # ["gcjs_dingdianchouqian_zhongbiao_gg","http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006002004&Paging=1",['name',  'ggstart_time', 'href',"info"],f1,f2],
    # ["gcjs_dingdianchouqian_biangeng_gg","http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006002002&Paging=1", ['name',  'ggstart_time', 'href',"info"],f1,f2],
    #
    # ["zfcg_zhaobiao_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001001&Paging=1", ['name',  'ggstart_time', 'href',"info"],f1,f2],
    ["zfcg_biangen_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001002&Paging=1", ['name',  'ggstart_time', 'href',"info"],f1,f2],
    # ["zfcg_zhongbiao_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001004&Paging=1", ['name',  'ggstart_time', 'href',"info"],f1,f2],
    # ["zfcg_liubiao_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001006&Paging=1",['name',  'ggstart_time', 'href',"info"],f1,f2],
    #
    # ["zfcg_feigong_zhaobiao_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007002001&Paging=1", ['name',  'ggstart_time', 'href',"info"],f1,f2],
    # ["zfcg_feigong_biangeng_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007002002&Paging=1", ['name',  'ggstart_time', 'href',"info"],f1,f2],
    # ["zfcg_feigong_zhongbiao_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007002004&Paging=1", ['name',  'ggstart_time', 'href',"info"],f1,f2],
    # ["zfcg_feigong_liubiao_gg", "http://www.tlzbcg.com/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007002006&Paging=1",['name',  'ggstart_time', 'href',"info"],f1,f2],
    #
    #
    # ["gcjs_yvcai_gg", "http://www.tlzbcg.com/tlsggzy/gcjs/006003/?Paging=1",['name',  'ggstart_time', 'href',"info"],f4,f2],
    # ["zfcg_yvcai_gg", "http://www.tlzbcg.com/tlsggzy/zfcg/007003/?Paging=1",['name',  'ggstart_time', 'href',"info"],f4,f2],
    # ["zfcg_dyxly_gg", "http://www.tlzbcg.com/tlsggzy/zfcg/007004/?Paging=1",['name',  'ggstart_time', 'href',"info"],f4,f2],


    # ["gcjs_zhaobiao_gg_yaq", "http://yaq.tlzbcg.com/yaqztb/jyxx/008001/008001001/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["gcjs_zhongbiaohx_gg_yaq", "http://yaq.tlzbcg.com/yaqztb/jyxx/008001/008001003/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["gcjs_zhongbiao_gg_yaq", "http://yaq.tlzbcg.com/yaqztb/jyxx/008001/008001004/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["gcjs_liubiao_gg_yaq", "http://yaq.tlzbcg.com/yaqztb/jyxx/008001/008001005/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    #
    # ["zfcg_zhaobiao_gg_yaq", "http://yaq.tlzbcg.com/yaqztb/jyxx/008002/008002001/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["zfcg_biangen_gg_yaq", "http://yaq.tlzbcg.com/yaqztb/jyxx/008002/008002002/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["zfcg_zhongbiao_gg_yaq", "http://yaq.tlzbcg.com/yaqztb/jyxx/008002/008002003/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["zfcg_liubiao_gg_yaq", "http://yaq.tlzbcg.com/yaqztb/jyxx/008002/008002004/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    #
    #
    # ["gcjs_zhaobiao_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008001/008001001/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["gcjs_zhongbiaohx_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008001/008001003/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["gcjs_zhongbiao_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008001/008001004/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["gcjs_liubiao_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008001/008001005/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    #
    # ["zfcg_zhaobiao_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008002/008002001/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["zfcg_dayibiangeng_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008002/008002002/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["zfcg_zhongbiao_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008002/008002003/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["zfcg_dyxly_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008002/008002004/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["zfcg_liubiao_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008002/008002005/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    #
    # ["qsy_zhaobiao_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008005/008005001/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["qsy_zhongbiao_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008005/008005004/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],
    # ["qsy_liubiao_gg_zyx", "http://zyx.tlzbcg.com/zyxztb/jyxx/008005/008005005/?Paging=1",['name',  'ggstart_time', 'href',"info"],f5,f2],

]

def work(conp):
    gg_meta(conp,data=data,diqu="安徽省铜陵市")

    # gg_html(conp,f=f3)


work(conp=["postgres","since2015","192.168.3.171","anhui","tongling"])

