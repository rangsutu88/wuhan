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
    "num":3,
    # 'total':2


    }
    m=web()
    m.write(**setting)


def f1(driver,num):
    driver.implicitly_wait(5)
    locator = (By.XPATH, '/html/body/div/div[7]/div[3]/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    # 寻找当前页
    cnum = driver.find_element_by_xpath('/html/body/div/div[7]/div[3]/table/tbody/tr[21]/td/div/div').text.strip()
    cnum = re.findall('记录 (\d+?)\/', cnum)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('/html/body/div/div[7]/div[3]/table/tbody/tr[1]/td[2]/a').text

        driver.execute_script("location.href=encodeURI('index_{}.jhtml');".format(num))

        locator = (
        By.XPATH, '/html/body/div/div[7]/div[3]/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    one = driver.find_element_by_xpath('/html/body/div/div[7]/div[3]/table/tbody/tr[1]/td[2]/a').text
    print(one)
    if '三亚市' in one:
        data=[]
        tmp=[one,None,None]
        data.append(tmp)
        df=pd.DataFrame(data)
        return df
    else:
        return

def f2(driver):
    driver.implicitly_wait(10)

    locator = (By.XPATH, '/html/body/div/div[7]/div[3]/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    total = 31
    return total

def work(conp,i=-1):
    data=[
        #
        ["gg","http://zw.hainan.gov.cn/ggzy/syggzy/GGjxzbgs1/index.jhtml",["name","ggstart_time","href"]],



    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
# conp=["postgres","since2015","192.168.3.171","jiangxi","shangrao"]

work(conp=conp)