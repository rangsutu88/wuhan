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


from lch.zhulong import est_tbs, est_meta, est_html, est_gg

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='zhangshu'


def f1(driver,num):
    locator = (By.XPATH,
               '//table[@class="bg04"]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    cnum = re.findall('_(\d+)___.html', url)[0]
    if int(cnum) != num:
        s = "_%d___.html" % num
        url = re.sub("_[0-9]+___.html", s, url)

        val = driver.find_element_by_xpath(
            "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/a").text
        driver.get(url)

        locator = (
            By.XPATH,
            "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/a[string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    url=driver.current_url

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
    df["info"] = None
    return df




def f2(driver):

    locator = (By.XPATH,
               '//table[@class="bg04"]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath(
            "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr[2]/td/a[last()]").get_attribute('href')
        total = re.findall('_(\d+)___.html', page)[0]

    except:
        total = 1

    total=int(total)
    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//table[@class="bg04"]')

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
    div = soup.find('td',id="newscontent")
    return div

data=[

    ["qsy_zhao_gg","http://www.zsggzy.com/news_,11,12,25,_%C6%E4%CB%FC_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["qita_zhao_gg","http://www.zsggzy.com/news_,11,12,73,_%C6%E4%CB%FB%D5%D0%B1%EA_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["qsy_zhong_gg","http://www.zsggzy.com/news_,11,13,33,_%C6%E4%CB%FC_1___.html",["name","ggstart_time","href",'info'],f1,f2],
    ["qita_zhong_gg","http://www.zsggzy.com/news_,11,13,78,_%C6%E4%CB%FB%D6%D0%B1%EA_1___.html",["name","ggstart_time","href",'info'],f1,f2],



    ["gcjs_fangjianshizheng_zhao_gg","http://www.zsggzy.com/news_,11,12,21,_%CA%D0%D5%FE%D4%B0%C1%D6_1___.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_fangjianshizheng_zhong_gg","http://www.zsggzy.com/news_,11,13,29,_%CA%D0%D5%FE%D4%B0%C1%D6_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["gcjs_zhao_gg","http://www.zsggzy.com/news_,11,12,18,_%BD%A8%C9%E8%B9%A4%B3%CC_1___.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_zhong_gg","http://www.zsggzy.com/news_,11,13,26,_%BD%A8%C9%E8%B9%A4%B3%CC_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["gcjs_jiaotong_zhao_gg","http://www.zsggzy.com/news_,11,12,19,_%B9%AB%C2%B7%BD%BB%CD%A8_1___.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_jiaotong_zhong_gg","http://www.zsggzy.com/news_,11,13,27,_%B9%AB%C2%B7%BD%BB%CD%A8_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["gcjs_shuili_zhao_gg","http://www.zsggzy.com/news_,11,12,20,_%CB%AE%C0%FB%B9%A4%B3%CC_1___.html",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_shuili_zhong_gg","http://www.zsggzy.com/news_,11,13,28,_%CB%AE%C0%FB%B9%A4%B3%CC_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["zfcg_zhao_gg","http://www.zsggzy.com/news_,11,12,22,_%D5%FE%B8%AE%B2%C9%B9%BA_1___.html",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhong_gg","http://www.zsggzy.com/news_,11,13,30,_%D5%FE%B8%AE%B2%C9%B9%BA_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["seji_zhao_gg","http://www.zsggzy.com/news_,11,12,69,_%C9%E8%BC%C6%D5%D0%B1%EA_1___.html",["name","ggstart_time","href",'info'],f1,f2],
    ["seji_zhong_gg","http://www.zsggzy.com/news_,11,13,74,_%C9%E8%BC%C6%D6%D0%B1%EA_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["jianli_zhao_gg","http://www.zsggzy.com/news_,11,12,70,_%BC%E0%C0%ED%D5%D0%B1%EA_1___.html",["name","ggstart_time","href",'info'],f1,f2],
    ["jianli_zhong_gg","http://www.zsggzy.com/news_,11,13,75,_%BC%E0%C0%ED%D6%D0%B1%EA_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["shigong_zhao_gg","http://www.zsggzy.com/news_,11,12,71,_%CA%A9%B9%A4%D5%D0%B1%EA_1___.html",["name","ggstart_time","href",'info'],f1,f2],
    ["shigong_zhong_gg","http://www.zsggzy.com/news_,11,13,76,_%CA%A9%B9%A4%D6%D0%B1%EA_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["kancha_zhao_gg","http://www.zsggzy.com/news_,11,12,72,_%CA%A9%B9%A4%D5%D0%B1%EA_1___.html",["name","ggstart_time","href",'info'],f1,f2],
    ["kancha_zhong_gg","http://www.zsggzy.com/news_,11,13,77,_%BF%B1%B2%EC%D6%D0%B1%EA_1___.html",["name","ggstart_time","href",'info'],f1,f2],

    ["dayi_gg","http://www.zsggzy.com/news_,11,14,_%B4%F0%D2%C9%B3%CE%C7%E5_1___.html",["name","ggstart_time","href",'info'],f1,f2],



]
def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省樟树市",**args)
    est_html(conp,f=f3,**args)
    # est_gg(conp,diqu="江西省樟树市")


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","jiangxi","zhangshu"]

    work(conp=conp)