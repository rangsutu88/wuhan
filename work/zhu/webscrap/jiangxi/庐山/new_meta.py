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


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


def f1(driver,num):
    driver.maximize_window()
    locator = (By.XPATH, "//div[@class='xxgk_navli'][1]/ul/li[3]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    cnum=driver.find_element_by_xpath("//span[@class='current']").text
    if int(cnum) != num:
        val = driver.find_element_by_xpath("//div[@class='xxgk_navli'][1]/ul/li[3]/a").text
        cpage = driver.find_element_by_xpath("//span[@class='inputBar']/input")
        cpage.clear()
        cpage.send_keys(num, Keys.ENTER)
        locator = (By.XPATH, "//div[@class='xxgk_navli'][1]/ul/li[3]/a[not(contains(string(),'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data=[]
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_='xxgk_navli')
    for div in divs:
        lis = div.find_all('li')
        index = lis[1].get_text()
        href = lis[2].a['href']
        name = lis[2].a.get_text()
        ggstart_time = lis[3].get_text()


        tmp = [index,name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    driver.maximize_window()

    locator = (By.XPATH, "//div[@class='xxgk_navli'][1]/ul/li[3]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    total = driver.find_element_by_xpath('//*[@id="page_public_info"]/a[last()]').get_attribute('paged')
    total=int(total)
    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="contentxxgk"]')

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
    div = soup.find('div',class_='wzcon fontContent j-fontContent')
    return div

data=[
    #
    ["gcjs_gg","http://www.lushan.gov.cn/public/column/4443193?type=4&catId=5337461&action=list",["index_num","name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.lushan.gov.cn/public/column/4443193?type=4&catId=5337475&action=list",["index_num","name","ggstart_time","href",'info'],f1,f2],

    ["zfcg_gg","http://www.lushan.gov.cn/public/column/4443193?type=4&catId=5336732&action=list",["index_num","name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.lushan.gov.cn/public/column/4443193?type=4&catId=5337407&action=list",["index_num","name","ggstart_time","href",'info'],f1,f2],


]

def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省庐山市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    # conp=["testor","zhulong","192.168.3.171","test","lch"]
    # conp=["testor","zhulong","192.168.3.171","test","public"]
    conp=["postgres","since2015","192.168.3.171","jiangxi","lushan"]

    work(conp=conp)