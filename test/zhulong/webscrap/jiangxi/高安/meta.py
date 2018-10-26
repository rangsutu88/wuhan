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
    # 'total':4


    }
    m=web()
    m.write(**setting)


def f1(driver,num):
    locator = (By.XPATH, '//*[@id="infolist"]/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    url = driver.current_url
    if "secondpageJyMk.html" in url:
        cnum = 1
    else:
        cnum = int(re.findall(r"/([0-9]{1,}).html", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub(r"[0-9]*.html", "secondpageJyMk.html", url)
        else:
            # s = r"/%d.html" % (num) if num > 1 else "secondpageJyMk.html"
            s = "/%d.html" % (num)
            url = url.rsplit('/', maxsplit=1)[0] + s
        val = driver.find_element_by_xpath('//*[@id="infolist"]/li[1]/div/a').text
        # print(val)
        driver.get(url)

        locator = (By.XPATH, "//*[@id='infolist']/li[1]/div/a[string()!='%s']"%val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('ul', class_='wb-data-item')
    data = []
    # url = driver.current_url

    urs = trs.find_all('li')
    for tr in urs:
        href = tr.a['href'].strip('.')
        if 'http' in href:
            href=href
        else:
            href = 'http://www.gaztbw.gov.cn' + href
        title = tr.a.get_text()
        date_time = tr.span.get_text()
        tmp = [title, date_time,href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df


def f2(driver):
    url = driver.current_url
    if url=='http://www.gaztbw.gov.cn/jyxx/001004/001004002/secondpageJyMk.html':
        total=1
        return total
    locator = (By.XPATH, '//*[@id="infolist"]/li[1]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//*[@id="page"]/ul/li[10]/a').text
    except:
        page=driver.find_element_by_xpath("//ul[@class='m-pagination-page']/li[last()]").text

    total=int(page)
    return total

def work(conp,i=-1):
    data=[
        #
        # ["gcjs_fangjianshizheng_zhaobiao_gg","http://www.gaztbw.gov.cn/jyxx/001001/001001001/secondpageJyMk.html",["name","ggstart_time","href"]],
        # ["gcjs_fangjianshizheng_zhongbiaohx_gg","http://www.gaztbw.gov.cn/jyxx/001001/001001004/secondpageJyMk.html",["name","ggstart_time","href"]],

        # ["gcjs_jiaotong_zhaobiao_gg","http://www.gaztbw.gov.cn/jyxx/001002/001002001/secondpageJyMk.html",["name","ggstart_time","href"]],
        # ["gcjs_jiaotong_zhongbiaohx_gg","http://www.gaztbw.gov.cn/jyxx/001002/001002003/secondpageJyMk.html",["name","ggstart_time","href"]],
        #
        # ["gcjs_shuili_zhaobiao_gg","http://www.gaztbw.gov.cn/jyxx/001003/001003001/secondpageJyMk.html",["name","ggstart_time","href"]],
        # ["gcjs_shuili_zhongbiaohx_gg","http://www.gaztbw.gov.cn/jyxx/001003/001003004/secondpageJyMk.html",["name","ggstart_time","href"]],
        #
        # ["zfcg_zhaobiao_gg","http://www.gaztbw.gov.cn/jyxx/001004/001004001/secondpageJyMk.html",["name","ggstart_time","href"]],
        # ["zfcg_zhongbiao_gg","http://www.gaztbw.gov.cn/jyxx/001004/001004004/secondpageJyMk.html",["name","ggstart_time","href"]],
        ["zfcg_biangeng_gg","http://www.gaztbw.gov.cn/jyxx/001004/001004002/secondpageJyMk.html",["name","ggstart_time","href"]],

        ["qita_zhaobiao_gg","http://www.gaztbw.gov.cn/jyxx/001008/001008001/secondpageJyMk.html",["name","ggstart_time","href"]],
        ["qita_zhongbiaohx_gg","http://www.gaztbw.gov.cn/jyxx/001008/001008002/secondpageJyMk.html",["name","ggstart_time","href"]],



    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","gaoan"]

work(conp=conp)