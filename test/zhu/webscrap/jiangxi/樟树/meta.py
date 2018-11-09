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
    locator = (By.XPATH,
               '/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    mark = re.findall('news_,(.+),_', url)[0]
    if mark=='11,12,25':
        locator = (By.XPATH,
                   '/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        print(num)
        if num <= 4:
            page = re.findall('_(\d+)___.html', url)[0]
            if int(page) != num:
                s = "_%d___.html" % num
                url = re.sub("_[0-9]+___.html", s, url)

                val = driver.find_element_by_xpath(
                    "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a").text
                driver.get(url)

                locator = (
                By.XPATH, "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a[string()!='%s']" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        else:
            print('-----two-----',num)
            two_num=num-4
            two_url='http://www.zsggzy.com/news_,11,12,73,_%C6%E4%CB%FB%D5%D0%B1%EA_1___.html'
            s = "_%d___.html"%two_num
            url = re.sub("_[0-9]+___.html", s, two_url)

            val = driver.find_element_by_xpath(
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a").text
            # print(url)
            driver.get(url)

            locator = (
                By.XPATH,
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    elif mark=='11,12,73':
        num=num-4
        page = re.findall('_(\d+)___.html', url)[0]
        if int(page) != num:
            s = "_%d___.html" % num
            url = re.sub("_[0-9]+___.html", s, url)

            val = driver.find_element_by_xpath(
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a").text
            driver.get(url)

            locator = (
            By.XPATH, "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    elif mark=='11,13,33':
        locator = (By.XPATH,
                   '/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        print(num)
        if num <= 3:
            page = re.findall('_(\d+)___.html', url)[0]
            if int(page) != num:
                s = "_%d___.html" % num
                url = re.sub("_[0-9]+___.html", s, url)

                val = driver.find_element_by_xpath(
                    "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a").text
                driver.get(url)

                locator = (
                By.XPATH, "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a[string()!='%s']" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        else:
            print('-----two-----',num)
            two_num=num-3
            two_url='http://www.zsggzy.com/news_,11,13,78,_%C6%E4%CB%FB%D5%D0%B1%EA_1___.html'
            s = "_%d___.html"%two_num
            url = re.sub("_[0-9]+___.html", s, two_url)

            val = driver.find_element_by_xpath(
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a").text
            # print(url)
            driver.get(url)

            locator = (
                By.XPATH,
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    elif mark=='11,13,78':
        num=num-3
        page = re.findall('_(\d+)___.html', url)[0]
        if int(page) != num:
            s = "_%d___.html" % num
            url = re.sub("_[0-9]+___.html", s, url)

            val = driver.find_element_by_xpath(
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a").text
            driver.get(url)

            locator = (
            By.XPATH, "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    else:
        page = re.findall('_(\d+)___.html', url)[0]
        if int(page) != num:
            s = "_%d___.html" % num
            url = re.sub("_[0-9]+___.html", s, url)

            val = driver.find_element_by_xpath(
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a").text
            driver.get(url)

            locator = (
                By.XPATH,
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    url=driver.current_url
    print(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find('table', attrs={'width': 650})
    trs = tables.find_all('tr')
    data=[]

    for i in range(0, len(trs), 2):
        tr = trs[i]
        href = tr.td.a['href']
        href = 'http://www.zsggzy.com/' + href
        name = tr.td.a.get_text()
        ggstart_time = tr.find('td', class_='newsdate').get_text().strip(']').strip('[')

        tmp = [name, ggstart_time,href]

        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df




def f2(driver):
    url=driver.current_url
    if url=='http://www.zsggzy.com/news_,11,12,25,_%C6%E4%CB%FC_1___.html':

        locator = (By.XPATH,'/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            page = driver.find_element_by_xpath(
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr[2]/td/a[last()]").get_attribute('href')
            total_1 = re.findall('_(\d+)___.html', page)[0]
            print(total_1)
        except:
            total_1=1

        val = driver.find_element_by_xpath(
            "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a").text
        driver.get('http://www.zsggzy.com/news_,11,12,73,_%C6%E4%CB%FB%D5%D0%B1%EA_1___.html')
        locator = (
            By.XPATH,
            "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a[string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            page = driver.find_element_by_xpath(
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr[2]/td/a[last()]").get_attribute('href')
            total_2 = re.findall('_(\d+)___.html', page)[0]
            print(total_2)
        except:

            total_2=1
        total=int(total_1)+int(total_2)

    elif url=='http://www.zsggzy.com/news_,11,13,33,_%C6%E4%CB%FC_1___.html':
        locator = (By.XPATH,
                   '/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            page = driver.find_element_by_xpath(
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr[2]/td/a[last()]").get_attribute('href')
            total_1 = re.findall('_(\d+)___.html', page)[0]
            print(total_1)
        except:
            total_1 = 1

        val = driver.find_element_by_xpath(
            "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a").text

        driver.get('http://www.zsggzy.com/news_,11,13,78,_%C6%E4%CB%FB%D6%D0%B1%EA_1___.html')
        locator = (
            By.XPATH,
            "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a[string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            page = driver.find_element_by_xpath(
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr[2]/td/a[last()]").get_attribute('href')
            total_2 = re.findall('_(\d+)___.html', page)[0]
            print(total_2)
        except:

            total_2 = 1
        total = int(total_1) + int(total_2)


    else:
        locator = (By.XPATH,
                   '/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            page = driver.find_element_by_xpath(
                "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr[2]/td/a[last()]").get_attribute('href')
            total = re.findall('_(\d+)___.html', page)[0]
            print(total)
        except:
            total = 1


    total=int(total)
    return total

def work(conp,i=-1):
    data=[

        ["qita_zhaobiao_gg","http://www.zsggzy.com/news_,11,12,25,_%C6%E4%CB%FC_1___.html",["name","ggstart_time","href"]],
        ["qita_zhongbiao_gg","http://www.zsggzy.com/news_,11,13,33,_%C6%E4%CB%FC_1___.html",["name","ggstart_time","href"]],

        ["gcjs_fangjianshizheng_zhaobiao_gg","http://www.zsggzy.com/news_,11,12,21,_%CA%D0%D5%FE%D4%B0%C1%D6_1___.html",["name","ggstart_time","href"]],
        ["gcjs_fangjianshizheng_zhongbiao_gg","http://www.zsggzy.com/news_,11,13,29,_%CA%D0%D5%FE%D4%B0%C1%D6_1___.html",["name","ggstart_time","href"]],

        ["gcjs_zhaobiao_gg","http://www.zsggzy.com/news_,11,12,18,_%BD%A8%C9%E8%B9%A4%B3%CC_1___.html",["name","ggstart_time","href"]],
        ["gcjs_zhongbiao_gg","http://www.zsggzy.com/news_,11,13,26,_%BD%A8%C9%E8%B9%A4%B3%CC_1___.html",["name","ggstart_time","href"]],

        ["gcjs_jiaotong_zhaobiao_gg","http://www.zsggzy.com/news_,11,12,19,_%B9%AB%C2%B7%BD%BB%CD%A8_1___.html",["name","ggstart_time","href"]],
        ["gcjs_jiaotong__zhongbiao_gg","http://www.zsggzy.com/news_,11,13,27,_%B9%AB%C2%B7%BD%BB%CD%A8_1___.html",["name","ggstart_time","href"]],

        ["gcjs_shuili_zhaobiao_gg","http://www.zsggzy.com/news_,11,12,20,_%CB%AE%C0%FB%B9%A4%B3%CC_1___.html",["name","ggstart_time","href"]],
        ["gcjs_shuili_zhongbiao_gg","http://www.zsggzy.com/news_,11,13,28,_%CB%AE%C0%FB%B9%A4%B3%CC_1___.html",["name","ggstart_time","href"]],

        ["zfcg_zhaobiao_gg","http://www.zsggzy.com/news_,11,12,22,_%D5%FE%B8%AE%B2%C9%B9%BA_1___.html",["name","ggstart_time","href"]],
        ["zfcg_zhongbiao_gg","http://www.zsggzy.com/news_,11,13,30,_%D5%FE%B8%AE%B2%C9%B9%BA_1___.html",["name","ggstart_time","href"]],

        ["seji_zhaobiao_gg","http://www.zsggzy.com/news_,11,12,69,_%C9%E8%BC%C6%D5%D0%B1%EA_1___.html",["name","ggstart_time","href"]],
        ["seji_zhongbiao_gg","http://www.zsggzy.com/news_,11,13,74,_%C9%E8%BC%C6%D6%D0%B1%EA_1___.html",["name","ggstart_time","href"]],

        ["jianli_zhaobiao_gg","http://www.zsggzy.com/news_,11,12,70,_%BC%E0%C0%ED%D5%D0%B1%EA_1___.html",["name","ggstart_time","href"]],
        ["jianli_zhongbiao_gg","http://www.zsggzy.com/news_,11,13,75,_%BC%E0%C0%ED%D6%D0%B1%EA_1___.html",["name","ggstart_time","href"]],

        ["shigong_zhaobiao_gg","http://www.zsggzy.com/news_,11,12,71,_%CA%A9%B9%A4%D5%D0%B1%EA_1___.html",["name","ggstart_time","href"]],
        ["shigong_zhongbiao_gg","http://www.zsggzy.com/news_,11,13,76,_%CA%A9%B9%A4%D6%D0%B1%EA_1___.html",["name","ggstart_time","href"]],

        ["kancha_zhaobiao_gg","http://www.zsggzy.com/news_,11,12,72,_%CA%A9%B9%A4%D5%D0%B1%EA_1___.html",["name","ggstart_time","href"]],
        ["kancha_zhongbiao_gg","http://www.zsggzy.com/news_,11,13,77,_%BF%B1%B2%EC%D6%D0%B1%EA_1___.html",["name","ggstart_time","href"]],

        ["dayi_gg","http://www.zsggzy.com/news_,11,14,_%B4%F0%D2%C9%B3%CE%C7%E5_1___.html",["name","ggstart_time","href"]],



    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","zhangshu"]

work(conp=conp)