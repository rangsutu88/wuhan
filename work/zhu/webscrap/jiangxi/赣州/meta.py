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


from zhulong.util.etl import est_tbs,est_meta,est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://www.gzzbtbzx.com/more.asp?id=5&city=1"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



def f1(driver,num):
    mark_url=driver.current_url
    if 'id' in mark_url:
        locator=(By.XPATH,'//td[@bgcolor="#DFDFDF"]/table[3]/tbody/tr/td/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        mark = re.findall(r'(id=\d+)', mark_url)[0]
        mark_2=re.findall(r'(city=\d+)',mark_url)[0]
        r_url = f3(mark,mark_2, num)

        val = driver.find_element_by_xpath('//td[@bgcolor="#DFDFDF"]/table[3]/tbody/tr/td/a').text

        driver.get(r_url)

        try:
            locator = (By.XPATH, '//td[@bgcolor="#DFDFDF"]/table[3]/tbody/tr/td/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(1)


        main_url = driver.current_url
        if 'id' in main_url:
            df=parse_1(driver)
        elif 'dq' in main_url:
            df=parse_2(driver)

        return df

    elif 'dq' in mark_url:
        locator = (By.XPATH, "//td[@bgcolor='#DFDFDF']/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        mark = re.findall(r'(dq=\d+)', mark_url)[0]
        mark_2 = re.findall(r'(dq=\d+)', mark_url)[0]
        r_url=f3(mark,mark_2,num)

        val = driver.find_element_by_xpath("//td[@bgcolor='#DFDFDF']/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a").text
        driver.get(r_url)
        try:
            locator = (By.XPATH,
             '//td[@bgcolor="#DFDFDF"]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(1)

        main_url = driver.current_url

        if 'id' in main_url:
            df=parse_1(driver)
        elif 'dq' in main_url:
            df=parse_2(driver)

        return df


def parse_1(driver):
    main_url = driver.current_url

    # print('----1111------', main_url)
    main_url = main_url.rsplit('/', maxsplit=1)[0]
    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find('td', attrs={'bgcolor': '#DFDFDF'})
    tables = content.find_all('table')
    for i in range(2, len(tables) - 1):
        table = tables[i]
        tr = table.find('tr')
        tds = tr.find_all('td')
        href = tds[0].a['href']
        if 'http' in href:
            href = href
        else:
            href = main_url + '/' + href
        name = tds[0].a.get_text()
        ggstart_time = tds[1].get_text()
        click_num = tds[2].get_text()
        tmp = [name, ggstart_time, click_num, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df
def parse_2(driver):
    main_url = driver.current_url

    # print('----2222----------------------------------------------', main_url)
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
        tmp = [ name, ggstart_time, click_num,href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df





data=[
    #
    ["gcjs_zhaobiao_gg","http://www.gzzbtbzx.com/more.asp?id=12&city=1",["name","ggstart_time","click_num","href",'info'],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.gzzbtbzx.com/more.asp?id=13&city=1",["name","ggstart_time","click_num","href",'info'],f1,f2],
    ["gcjs_dayibucong_gg","http://www.gzzbtbzx.com/more.asp?id=41&city=1",["name","ggstart_time","click_num","href",'info'],f1,f2],
    #
    #
    ["zfcg_zhaobiao_gg","http://www.gzzbtbzx.com/more.asp?id=2&city=1",["name","ggstart_time","click_num","href",'info'],f1,f2],
    ["zfcg_bumen_gg","http://www.gzzbtbzx.com/more.asp?id=5&city=1",["name","ggstart_time","click_num","href",'info'],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.gzzbtbzx.com/more.asp?id=3&city=1",["name","ggstart_time","click_num","href",'info'],f1,f2],

]

def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省赣州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    # conp=["testor","zhulong","192.168.3.171","test","lch"]
    # conp=["testor","zhulong","192.168.3.171","test","public"]
    conp=["postgres","since2015","192.168.3.171","jiangxi","ganzhou"]

    work(conp=conp)