import time
from os.path import join, dirname

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


from zhulong.util.etl import est_tbs, est_meta, est_html, gg_existed


# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


_name_='jian'


def chang_address(driver,i,c_text):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]

    if cc_text != c_text:
        val = driver.find_element_by_xpath("//div[@class='pagingList']/ul/li/a").text
        driver.find_element_by_xpath("//div[@class='pagingTitle-list']/ul/li[{num}]/a".format(num=i)).click()
        try:
            locator = (By.XPATH, "//div[@class='pagingList']/ul/li/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(locator)
        except:
            time.sleep(2)


def chang_page(driver,num):
    try:
        cnum = driver.find_element_by_xpath('//a[@class="curpage"]').text
    except:
        cnum=1

    url=driver.current_url
    main_url=url.rsplit('/',maxsplit=1)[0]
    if int(cnum) != num:
        if num==1:
            url=main_url+'/index.htm'
        else:
            url=main_url+'/index_'+str(num-1)+'.htm'
        val=driver.find_element_by_xpath('//div[@class="pagingList"]/ul/li[1]/a').text

        driver.get(url)
        locator=(By.XPATH,'//div[@class="pagingList"]/ul/li[1]/a')
        WebDriverWait(driver, 10).until_not(EC.text_to_be_present_in_element(locator,val))


def f1(driver,num):
    locator=(By.XPATH,'//div[@class="pagingList"]/ul/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    c_text=driver.find_element_by_xpath('//div[@class="titleMessageLeft fl"]').text.strip()

    for i in range(1, int(len(PAGE)) + 1):
        if sum(PAGE[:i - 1]) < num <= sum(PAGE[:i]):
            num = num - sum(PAGE[:i - 1])

            # 增量更新
            if num > CDC_NUM : return

            chang_address(driver, i, c_text)
            chang_page(driver, num)
            is_useful = True
            break

    if 'is_useful' not in locals():
        print('页数不合法%d' % num)
        return


    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('div', class_='pagingList')
    data = []
    url = driver.current_url
    rindex = url.rfind('/')
    main_url = url[:rindex]
    urs = trs.find_all('li')
    for tr in urs:
        href = tr.a['href'].strip('.')
        name = tr.a.get_text()
        ggstart_time = tr.span.get_text()

        if re.findall('http', href):
            href = href
        else:
            href = main_url + href
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    global PAGE
    global CC_TEXT
    PAGE=[]
    CC_TEXT=[]

    locator = (By.XPATH, "//div[@class='pagingList']/ul/li/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    for i in range(1,13):

        val = driver.find_element_by_xpath("//div[@class='pagingList']/ul/li/a").text
        driver.find_element_by_xpath("//div[@class='pagingTitle-list']/ul/li[{num}]/a".format(num=i)).click()
        try:
            locator = (By.XPATH, "//div[@class='pagingList']/ul/li/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver,10).until(locator)
        except:
            time.sleep(2)
        try:
            page = driver.find_element_by_xpath('//*[@id="div_page"]/a[last()]').get_attribute('href')
            total_ = re.findall(r'index_(\d+).htm', page)[0]
        except:
            total_=0

        cc_text=driver.find_element_by_xpath('//div[@class="titleMessageLeft fl"]').text.strip()
        total_ = int(total_) + 1
        PAGE.append(total_)
        CC_TEXT.append(cc_text)

    total=sum(PAGE)
    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="text-main"]')

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
    div = soup.find('div',class_='text-main')
    return div



data=[
    #
    ["gcjs_zhaobiao_gg","http://www.japrtc.gov.cn/jyxx/jsgc/zbgg/",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_zhongbiaohx_gg","http://www.japrtc.gov.cn/jyxx/jsgc/zbgs/",["name","ggstart_time","href",'info'],f1,f2],
    ["gcjs_dayibucong_gg","http://www.japrtc.gov.cn/jyxx/jsgc/dyby/",["name","ggstart_time","href",'info'],f1,f2],


    ["zfcg_zhaobiao_gg","http://www.japrtc.gov.cn/jyxx/zfcg/zbgg/",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_dayibucong_gg","http://www.japrtc.gov.cn/jyxx/zfcg/dyby/",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhongbiao_gg","http://www.japrtc.gov.cn/jyxx/zfcg/zbgs/",["name","ggstart_time","href",'info'],f1,f2],

]


def get_profile():
    path1 = join(dirname(__file__), 'profile')
    with open(path1, 'r') as f:
        p = f.read()

    return p


def get_conp(txt):
    x = get_profile() + ',' + txt
    arr = x.split(',')
    return arr


if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 5
else:
    CDC_NUM = 10000


def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省吉安市",**args)
    # est_html(conp,f=f3,**args)


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","jiangxi","jian"]

    work(conp=conp,cdc_total=None)