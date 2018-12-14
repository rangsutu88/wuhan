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


from zhulong.util.etl import est_tbs, est_meta, est_html, est_gg


# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='tengchong'


def f1(driver,num):
    locator = (By.XPATH, '//div[@class="boxcontent"]/table/tbody/tr[2]/td[3]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    try:
        cnum = driver.find_element_by_xpath('//span[@id="lblAjax_PageIndex"]').text
    except:
        cnum=1

    if cnum == '':cnum=1
    if int(cnum) != num:
        val = driver.find_element_by_xpath('//div[@class="boxcontent"]/table/tbody/tr[2]/td[3]').text

        input_page = driver.find_element_by_xpath('//div[@class="pager"]/table/tbody/tr/td[1]/input')
        input_page.clear()
        input_page.send_keys(num, Keys.ENTER)

        locator = (By.XPATH, '//div[@class="boxcontent"]/table/tbody/tr[2]/td[3][not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_='boxcontent').find('table')
    trs = div.find_all('tr')
    data = []

    for i in range(1, len(trs)):
        tr = trs[i]
        tds = tr.find_all('td')
        href = tds[2].a['href']
        name = tds[2].a.get_text()
        index_num = tds[1].get_text()
        ggstart_time = tds[3].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.tcsggzyjyw.com/Jyweb/' + href
        if re.findall('SubType2=1$',url) or re.findall('SubType2=12$',url):

            ggend_time=tds[4].get_text()
            tmp = [index_num, name, href, ggstart_time, ggend_time]
        else:
            tmp = [index_num, name, href, ggstart_time]

        data.append(tmp)

    df=pd.DataFrame(data=data)
    df['info']=None
    return df



def f2(driver):
    locator = (By.XPATH, '//div[@class="boxcontent"]/table/tbody/tr[2]/td[3]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//span[@id="lblAjax_TotalPageCount"]').text
        total = int(page)
    except:
        total=1
    if total=='': total=1
    driver.quit()
    return total

def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//table[@class="table_a"] | //div[@id="Content_divPBGS"]'
                         ' |//div[@class="tableStyle"] | //div[@class="detail_contect"]')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

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
    div = soup.find('table',class_='table_a')
    if div == None:
        div=soup.find('div',id="Content_divPBGS")
        if div == None:
            div = soup.find('div', class_="tableStyle")
            if div == None:
                div=soup.find('div', class_="detail_contect")

    return div

data=[
    #
    ["gcjs_zhaobiao_gg","http://www.tcsggzyjyw.com/Jyweb/ZBGGList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=1&SubType2=1",["index_num", "name", "href", "ggstart_time", "ggend_time","info"],f1,f2],
    ["zfcg_zhaobiao_gg","http://www.tcsggzyjyw.com/Jyweb/JYXTXXList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=2&SubType2=12",["index_num", "name", "href", "ggstart_time", "ggend_time","info"],f1,f2],

    ["gcjs_zhongbiaohx_gg","http://www.tcsggzyjyw.com/Jyweb/PBJGGSList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=1&SubType2=24",["index_num", "name", "href", "ggstart_time","info"],f1,f2],
    ["gcjs_zhongbiao_gg","http://www.tcsggzyjyw.com/Jyweb/PBJGGSList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=1&SubType2=11",["index_num", "name", "href", "ggstart_time","info"],f1,f2],
    ["gcjs_liubiao_gg","http://www.tcsggzyjyw.com/Jyweb/PBJGGSList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=1&SubType2=5",["index_num", "name", "href", "ggstart_time","info"],f1,f2],
    ["gcjs_fuhejieguo_gg","http://www.tcsggzyjyw.com/Jyweb/FHJGGSList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=1&SubType2=31",["index_num", "name", "href", "ggstart_time","info"],f1,f2],

    ["zfcg_zhongbiao_gg","http://www.tcsggzyjyw.com/Jyweb/JYXTXXList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=2&SubType2=14",["index_num", "name", "href", "ggstart_time","info"],f1,f2],
    ["zfcg_liubiao_gg","http://www.tcsggzyjyw.com/Jyweb/JYXTXXList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=2&SubType2=28",["index_num", "name", "href", "ggstart_time","info"],f1,f2],
    ["zfcg_fuhejieguo_gg","http://www.tcsggzyjyw.com/Jyweb/FHJGGSList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=2&SubType2=32",["index_num", "name", "href", "ggstart_time","info"],f1,f2],

    ["qsy_zhongbiao_gg","http://www.tcsggzyjyw.com/Jyweb/JYXTXXList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=5&SubType2=23",["index_num", "name", "href", "ggstart_time","info"],f1,f2],


]

def work(conp,**args):
    est_meta(conp,data=data,diqu="云南省腾冲市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","yunnan","tengchong"]

    work(conp=conp)