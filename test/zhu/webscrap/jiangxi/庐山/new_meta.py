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
    return df


def f2(driver):
    driver.maximize_window()

    locator = (By.XPATH, "//div[@class='xxgk_navli'][1]/ul/li[3]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    total = driver.find_element_by_xpath('//*[@id="page_public_info"]/a[last()]').get_attribute('paged')
    total=int(total)
    driver.quit()
    return total

def work(conp,i=-1):
    data=[
        #
        ["gcjs_gg","http://www.lushan.gov.cn/public/column/4443193?type=4&catId=5337461&action=list",["index_num","name","ggstart_time","href"]],
        ["gcjs_zhongbiaohx_gg","http://www.lushan.gov.cn/public/column/4443193?type=4&catId=5337475&action=list",["index_num","name","ggstart_time","href"]],

        ["zfcg_gg","http://www.lushan.gov.cn/public/column/4443193?type=4&catId=5336732&action=list",["index_num","name","ggstart_time","href"]],
        ["zfcg_zhongbiao_gg","http://www.lushan.gov.cn/public/column/4443193?type=4&catId=5337407&action=list",["index_num","name","ggstart_time","href"]],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","lushan"]

work(conp=conp)