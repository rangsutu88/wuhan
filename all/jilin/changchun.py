import time
from os.path import join, dirname

import pandas as pd
import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

from lch.zhulong import est_meta,est_html, gg_existed

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]

# #
# url="http://www.ccggzy.gov.cn/qxxxgk/003001/003001001/CountyZfcgNotice.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
# #

_name_='changchun'

def chang_address(driver,i,c_text):

    # 不是对应的的点击切换地区
    cc_text=CC_TEXT[i-1]

    if cc_text != c_text:
        try:
            val = driver.find_element_by_xpath('//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a').get_attribute(
            "href")[- 30:]

        except:
            driver.find_element_by_xpath('//span[@class="ewb-screen-name current"]')
            val='kong!!!'

        driver.find_element_by_xpath('(//div[@class="ewb-screen-list"])[1]/span[{}]'.format(i)).click()
        try:

            locator = (By.XPATH, '//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a[not(contains(@href,"%s"))]' % val)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            locator = (By.XPATH, '//span[@class="pg_maxpagenum"]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            time.sleep(1)
        except:
            driver.find_element_by_xpath('//span[@class="ewb-screen-name current"]')
            time.sleep(1)




def chang_page(driver,num):
    cnum = driver.find_element_by_xpath('//span[@class="pg_maxpagenum"]').text.strip()
    cnum = re.findall('(\d+)/', cnum)[0]
    if cnum != str(num):

        val = driver.find_element_by_xpath('//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a').get_attribute(
            "href")[- 30:]

        driver.find_element_by_xpath('//input[@class="pg_num_input"]').clear()
        driver.find_element_by_xpath('//input[@class="pg_num_input"]').send_keys(num)
        driver.find_element_by_xpath('//a[@class="pg_gobtn"]').click()

        locator = (By.XPATH, '//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f1(driver,num):


    try:
        locator = (By.XPATH, '//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        time.sleep(3)

    c_text = driver.find_element_by_xpath('//span[@class="ewb-screen-name current"]').text


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

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('tbody', id='showList')
    if div == None:
        div=soup.find('tbody', id='showlist')
    trs = div.find_all('tr')
    url = driver.current_url
    for tr in trs:

        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a.get_text().strip()

        if name.startswith('【'):
            gg_type = None if not re.findall(r'^【(.+?)】', name) else re.findall(r'^【(.+?)】', name)[0]
            name = name.split('】', maxsplit=1)[1]
        else:
            gg_type = None

        ggstart_time = tds[2].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.ccggzy.gov.cn' + href

        ccc_text = driver.find_element_by_xpath('//span[@class="ewb-screen-name current"]').text
        diqu_dict = {'diqu': ccc_text}
        info=json.dumps(diqu_dict,ensure_ascii=False)

        if '003002' in url:

            tmp = [name, ggstart_time, href,info]
        else:
            tmp = [gg_type, name, ggstart_time, href,info]

        data.append(tmp)
    df=pd.DataFrame(data=data)

    return df



def f2(driver):
    global PAGE
    global CC_TEXT
    PAGE=[]
    CC_TEXT = []
    try:
        locator = (By.XPATH, '//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        html=driver.page_source
        if '暂时没有内容' in html:
            time.sleep(3)
        else:
            raise TimeoutError

    for i in range(1, 17):
        if i != 1:
            try:
                time.sleep(0.5)
                val = driver.find_element_by_xpath('//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a').get_attribute(
            "href")[- 30:]
            except:
                time.sleep(1)
                html = driver.page_source
                if '暂时没有内容' in html:
                    time.sleep(1)
                else:
                    raise TimeoutError
                val = 'none!!!!!'

            driver.find_element_by_xpath('(//div[@class="ewb-screen-list"])[1]/span[{}]'.format(i)).click()
                #
            try:
                locator = (By.XPATH, '//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a[not(contains(@href,"%s"))]' % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
                locator = (By.XPATH, '//span[@class="pg_maxpagenum"]')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
                time.sleep(2)
            except:
                time.sleep(0.5)
                html = driver.page_source
                if '暂时没有内容' in html:
                    time.sleep(0.5)
                else:
                    raise TimeoutError


        try:
            page = driver.find_element_by_xpath('//span[@class="pg_maxpagenum"]').text.strip()
            total_ = int(re.findall('/(\d+)', page)[0])
        except:
            time.sleep(1)
            html = driver.page_source
            if '暂时没有内容' in html:
                time.sleep(0.5)
            else:
                raise TimeoutError
            total_=0
        cc_text = driver.find_element_by_xpath('//span[@class="ewb-screen-name current"]').text

        PAGE.append(total_)
        CC_TEXT.append(cc_text)

    total = sum(PAGE)
    driver.quit()

    return total

def f4(driver,num):
    if num > CDC_NUM: return

    locator = (By.XPATH, '//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, '//span[@class="pg_maxpagenum"]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum = driver.find_element_by_xpath('//span[@class="pg_maxpagenum"]').text.strip()
    cnum=re.findall('(\d+)/',cnum)[0]
    if cnum != str(num):
        val = driver.find_element_by_xpath('//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a').get_attribute(
            "href")[- 30:]

        driver.find_element_by_xpath('//input[@class="pg_num_input"]').clear()
        driver.find_element_by_xpath('//input[@class="pg_num_input"]').send_keys(num)
        driver.find_element_by_xpath('//a[@class="pg_gobtn"]').click()

        locator = (By.XPATH, '//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    data=[]
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('tbody', id='showList')
    trs = div.find_all('tr')
    url=driver.current_url
    for tr in trs:

        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a.get_text().strip()

        if name.startswith('【'):
            ggtype_ = None if not re.findall(r'^【(.+?)】', name) else re.findall(r'^【(.+?)】', name)[0]
            name = name.split('】', maxsplit=1)[1]
        else:
            ggtype_ = None

        ggstart_time = tds[2].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.ccggzy.gov.cn' + href
        if '002002' in url:
            tmp = [ name, ggstart_time, href]
        else:
            tmp = [ggtype_, name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    diqu_dict = {'diqu': '市级'}
    df["info"] = json.dumps(diqu_dict, ensure_ascii=False)

    return df

def f5(driver):
    locator = (By.XPATH, '//table[@class="ewb-table-info"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page = driver.find_element_by_xpath('//span[@class="pg_maxpagenum"]').text

    total = re.findall('/(\d+)', page)[0]
    total = int(total)
    driver.quit()

    return total


def f3(driver, url):

    driver.get(url)

    locator = (By.XPATH, '//div[@class="ewb-text-box"]')

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
    div = soup.find('div',class_='ewb-text-content ewb-row')
    return div




data=[
    ["zfcg_zhaobiao_diqu2_gg","http://www.ccggzy.gov.cn/qxxxgk/003001/003001001/CountyZfcgNotice.html",['gg_type',"name","ggstart_time","href","info"],f1,f2],
    ["zfcg_biangen_diqu2_gg","http://www.ccggzy.gov.cn/qxxxgk/003001/003001003/CountyZfcgNotice.html",['gg_type',"name","ggstart_time","href","info"],f1,f2],
    ["zfcg_zhongbiao_diqu2_gg","http://www.ccggzy.gov.cn/qxxxgk/003001/003001004/CountyZfcgNotice.html",['gg_type',"name","ggstart_time","href","info"],f1,f2],

    ["gcjs_zhaobiao_diqu2_gg","http://www.ccggzy.gov.cn/qxxxgk/003002/003002001/CountyPurhcaseNotice.html",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiaohx_diqu2_gg","http://www.ccggzy.gov.cn/qxxxgk/003002/003002002/CountyPurhcaseNotice.html",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_biangen_diqu2_gg","http://www.ccggzy.gov.cn/qxxxgk/003002/003002003/CountyPurhcaseNotice.html",["name","ggstart_time","href","info"],f1,f2],
    ["gcjs_zhongbiao_diqu2_gg","http://www.ccggzy.gov.cn/qxxxgk/003002/003002004/CountyPurhcaseNotice.html",["name","ggstart_time","href","info"],f1,f2],


    ["zfcg_yucai_diqu1_gg","http://www.ccggzy.gov.cn/sjxxgk/002001/002001002/CityZfcgNotice.html",["gg_type","name","ggstart_time","href","info"],f4,f5],
    ["zfcg_zhaobiao_diqu1_gg","http://www.ccggzy.gov.cn/sjxxgk/002001/002001001/CityZfcgNotice.html",['gg_type',"name","ggstart_time","href","info"],f4,f5],
    ["zfcg_biangen_diqu1_gg","http://www.ccggzy.gov.cn/sjxxgk/002001/002001003/CityZfcgNotice.html",['gg_type',"name","ggstart_time","href","info"],f4,f5],

    ["zfcg_jieguo_diqu1_gg","http://www.ccggzy.gov.cn/sjxxgk/002001/002001004/CityZfcgNotice.html",['gg_type',"name","ggstart_time","href","info"],f4,f5],

    ["gcjs_zhaobiao_diqu1_gg","http://www.ccggzy.gov.cn/sjxxgk/002002/002002001/CityPurchaseNotice.html",["name","ggstart_time","href","info"],f4,f5],
    ["gcjs_zhongbiaohx_diqu1_gg","http://www.ccggzy.gov.cn/sjxxgk/002002/002002002/CityPurchaseNotice.html",["name","ggstart_time","href","info"],f4,f5],
    ["gcjs_biangen_diqu1_gg","http://www.ccggzy.gov.cn/sjxxgk/002002/002002003/CityPurchaseNotice.html",["name","ggstart_time","href","info"],f4,f5],
    ["gcjs_zhongbiao_diqu1_gg","http://www.ccggzy.gov.cn/sjxxgk/002002/002002004/CityPurchaseNotice.html",["name","ggstart_time","href","info"],f4,f5],

]

# CDC_NUM=1000
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

#
def work(conp,**args):
    est_meta(conp,data=data,diqu="吉林省长春市",**args)
    est_html(conp,f=f3,**args)

# CDC_NUM 为增量更新页数,设置成总页数以上(如:10000)可爬全部
# 增量更新时,需将cdc_total设置成 None



if __name__=='__main__':

    work(conp=["postgres","since2015","192.168.3.171","jilin","changchun"],cdc_total=None,num=10)
    pass