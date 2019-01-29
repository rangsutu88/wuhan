import random
import time
from collections import OrderedDict

import pandas as pd

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from zhulong.util.etl import est_meta, est_html, add_info

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://dycg.dongying.gov.cn/BigClassList.aspx?BigClass=2&Zone=5&Type=1"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



_name_='dongying'

time_list=[2,]

def f1(driver,num):
    try:
        locator = (By.XPATH, '(//td[@class="linebottom1"])[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        alert = driver.switch_to.alert
        alert.accept()


    locator = (By.XPATH, '(//td[@class="linebottom1"])[2]/a')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    try:
        cnum=int(driver.find_element_by_xpath('//span[@id="Label1"]').text)
    except:
        alert = driver.switch_to.alert
        alert.accept()
        cnum = int(driver.find_element_by_xpath('//span[@id="Label1"]').text)

    EVENTTARGET_dict={
        'next':'LinkButton4',
        'previou':'LinkButton3',
        'first':'LinkButton2',
        'last':'LinkButton5'
    }

    while cnum != num:
        time.sleep(random.random()+sum(time_list))
        if cnum > num:

            if num < cnum - num:
                mark='first'

            else:
                mark='previou'

        else:
            if total-num < num -cnum:
                mark='last'

            else:
                mark='next'

        try:
            val = driver.find_element_by_xpath('(//td[@class="linebottom1"])[2]/a').get_attribute('href')[-30:]
            driver.execute_script("javascript:__doPostBack('{}','')".format(EVENTTARGET_dict[mark]))
        except:
            alert = driver.switch_to.alert
            alert.accept()
            val = driver.find_element_by_xpath('(//td[@class="linebottom1"])[2]/a').get_attribute('href')[-30:]
            driver.execute_script("javascript:__doPostBack('{}','')".format(EVENTTARGET_dict[mark]))

        try:
            locator = (By.XPATH, '(//td[@class="linebottom1"])[2]/a[not(contains(@href,"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except:
                if '403' in driver.title:
                    time_list.append(1)
                else:
                    raise TimeoutError


        locator = (By.XPATH, '(//td[@class="linebottom1"])[2]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        cnum=int(driver.find_element_by_xpath('//span[@id="Label1"]').text)

    content=driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    tds = soup.find_all('td', class_="linebottom1")
    data = []
    for i in range(0,len(tds),4):

        name =tds[i+1].a.get_text()
        href =tds[i+1].a['href']
        if 'http' in href:
            href=href
        else:
            href = 'http://dycg.dongying.gov.cn/' + href
        ggstart_time = tds[i+3].get_text()
        tmp = [name, ggstart_time, href]
        # print(tmp)
        data.append(tmp)

    df=pd.DataFrame(data=data)


    return df



def f2(driver):
    global total
    try:
        locator = (By.XPATH, '(//td[@class="linebottom1"])[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        alert = driver.switch_to.alert
        alert.accept()

    locator = (By.XPATH, '(//td[@class="linebottom1"])[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    total = driver.find_element_by_xpath('//span[@id="Label2"]').text
    total=int(total)

    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//td[@id="fontzoom"]')

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

    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('td', id="fontzoom")
    if div == None:
        raise ValueError('return div is None')

    return div
def get_data():
    data = []

    ggtype = OrderedDict([("zhaobiao", "1"),("biangengliubiao", "3"), ("zhongbiao", "2")])

    gctype = OrderedDict([('工程','2'),("货物", "1"), ("服务", "3"), ("询价", "4")])

    adtype = OrderedDict([('东营市','5'),("东营区", "6"), ("河口区", "7"), ("广饶县", "8"), ("垦利县", "9"),
                          ("利津县", "10"),("开发区", "11"),("东营港", "12"),("农高区", "13")])

    for w1 in ggtype.keys():
        for w2 in adtype.keys():
            for w3 in gctype.keys():
                href="http://dycg.dongying.gov.cn/BigClassList.aspx?BigClass={gc}&Zone={ad}&Type={gg}".format(gc=gctype[w3],gg=ggtype[w1],ad=adtype[w2])
                tmp=["zfcg_%s_diqu%s_type%s_gg"%(w1,adtype[w2],gctype[w3]),href,["name","ggstart_time","href",'info'],add_info(f1,{"jy_type":w3,"diqu":w2}),f2]

                data.append(tmp)

    remove_arr = ["zfcg_biangengliubiao_diqu9_type2_gg"]
    data1 = data.copy()
    for w in data:

        if w[0] in remove_arr: data1.remove(w)


    return data1

data=get_data()

def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省东营市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","lch","shandong_dongying"]

    work(conp=conp,pageloadstrategy='none',pageloadtimeout=60)