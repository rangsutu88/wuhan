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
    url=driver.current_url
    mark = re.findall('ClassID=(\d+)&', url)[0]
    print(mark)
    if mark=='19' or mark=='25':
        locator = (By.XPATH, "//td[@class='main_tdbg_575']/table/tbody/tr/td[2]/a[2]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    else:
        locator=(By.XPATH,"(//td[@class='main_tdbg_575']/a[2])")
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))


    cnum=int(re.findall("page=([0-9]{1,})",url)[0])

    if num!=cnum:

        s="page=%d"%(num)
        url=re.sub("page=[0-9]+",s,url)
        # print(url)
        if mark=='19' or mark=='25':
            val=driver.find_element_by_xpath("//td[@class='main_tdbg_575']/table/tbody/tr/td[2]/a[2]").text
            driver.get(url)
            locator=(By.XPATH,"(//td[@class='main_tdbg_575']/table/tbody/tr/td[2]/a[2])[not(contains(string(),'%s'))]"%val)
            WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
        else:
            val = driver.find_element_by_xpath("(//td[@class='main_tdbg_575']/a[2])").text
            driver.get(url)
            locator = (By.XPATH, "(//td[@class='main_tdbg_575']/a[2])[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find('td', class_='main_tdbg_575')
    tds = tables.find_all('a', attrs={'title': not None})
    data=[]
    for td in tds:

        href = td['href']
        href = 'http://www.fcgzj.gov.cn' + href
        content = td['title']
        name = re.findall('文章标题：(.+)', content)[0]
        ggstart_time = re.findall('更新时间：(\d+-\d+-\d)', content)[0]


        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):
    url = driver.current_url
    mark=re.findall('ClassID=(\d+)&',url)[0]
    print(mark)
    if mark=='19' or mark=='25':
        locator = (By.XPATH, "//td[@class='main_tdbg_575']/table/tbody/tr/td[2]/a[2]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    else:
        locator = (By.XPATH, "(//td[@class='main_tdbg_575']/a[2])")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    try:
        page = driver.find_element_by_xpath("//div[@class='show_page']/a[last()]").get_attribute('href')
        total = re.findall(r'page=(\d+)', page)[0]
        total=int(total)
    except:
        total=1
    return total

def work(conp,i=-1):
    data=[
        #
        # ["gcjs_zhaobiao_gg","http://www.fcgzj.gov.cn/Article/ShowClass.asp?ClassID=14&page=1",["name","ggstart_time","href"]],
        # ["gcjs_zhongbiaohx_gg","http://www.fcgzj.gov.cn/Article/ShowClass.asp?ClassID=20&page=1",["name","ggstart_time","href"]],

        # ["zfcg_zhaobiao_gg","http://www.fcgzj.gov.cn/Article/ShowClass.asp?ClassID=15&page=1",["name","ggstart_time","href"]],
        # ["zfcg_zhongbiao_gg","http://www.fcgzj.gov.cn/Article/ShowClass.asp?ClassID=21&page=1",["name","ggstart_time","href"]],

        #乡镇交易
        ["xzjy_zhaobiao_gg","http://www.fcgzj.gov.cn/Article/ShowClass.asp?ClassID=19&page=1",["name","ggstart_time","href"]],
        ["xzjy_zhongbiaohx_gg","http://www.fcgzj.gov.cn/Article/ShowClass.asp?ClassID=25&page=1",["name","ggstart_time","href"]],

        ["qita_zhaobiao_gg","http://www.fcgzj.gov.cn/Article/ShowClass.asp?ClassID=18&page=1",["name","ggstart_time","href"]],
        ["qita_zhongbiaohx_gg","http://www.fcgzj.gov.cn/Article/ShowClass.asp?ClassID=24&page=1",["name","ggstart_time","href"]],



    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","fengcheng"]

work(conp=conp)