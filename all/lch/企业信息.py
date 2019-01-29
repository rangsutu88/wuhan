import random
import time
from collections import OrderedDict

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
from selenium.webdriver.support.select import Select
import requests
import json
from fake_useragent import UserAgent


from lch.zhulong_l.util import est_meta

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]

# #
# url="http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


_name_=''



def f1(driver,num):


    locator = (By.XPATH, '(//td[@class="text-left primary"])[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    ua=UserAgent()
    cookies = driver.get_cookies()
    COOKIES = {}
    for cookie in cookies:
        COOKIES[cookie['name']] = cookie['value']

    if len(total_list)!=1:
        COOKIES['filter_comp']='show'

    headers={

    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "jzsc.mohurd.gov.cn",
    "Origin": "http://jzsc.mohurd.gov.cn",
    "Referer": "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list",
    "User-Agent": ua.chrome
    }

    for i in range(1, int(len(total_list)) + 1):
        if sum(total_list[:i - 1]) < num <= sum(total_list[:i]):
            num = num - sum(total_list[:i - 1])

            form_data = {

                "apt_code": apt_code_list[i-1],
                "qy_fr_name": "",
                "$total": total_count_list[i-1],
                "qy_reg_addr": qy_reg_addr_list[i-1],
                "qy_code": "",
                "qy_name": "",
                "$pgsz": 15,
                "apt_certno": "",
                "qy_region": qy_region_list[i-1],
                "$reload": 0,
                "qy_type": qy_type_list[i-1],
                "$pg": num,
                "qy_gljg": "",
                "apt_scope": apt_scope_list[i-1],
            }

            time.sleep(random.random())
            req=requests.post(url,data=form_data,headers=headers,cookies=COOKIES,timeout=20)

            if req.status_code != 200:
                print(req.text)
                raise ValueError('Error response status_code %s'%req.status_code)

    ht=req.text
    if '暂未查询到已登记入库信息' in ht:
        return pd.DataFrame(data=[['1','1','1','1','1',json.dumps({"hreftype":"不可抓网页"})],])

    soup = BeautifulSoup(ht, 'lxml')
    trs = soup.find('tbody', class_="cursorDefault").find_all('tr',recursive=False)

    data_ = []
    for tr in trs:
        tds=tr.find_all('td')
        credit_code=tds[1].get_text().strip()

        name = tds[2].a.get_text().strip()
        href = tds[2].a['href']
        if 'http' in href:
            href=href
        else:
            href="http://jzsc.mohurd.gov.cn"+href
        juridical_person=tds[3].get_text().strip()

        address=tds[4].get_text().strip()

        tmp = [credit_code,name,href,juridical_person,address,None]
        data_.append(tmp)
    # print(data_)
    df=pd.DataFrame(data=data_)

    return df



def f2(driver):

    total=sum(total_list)

    driver.quit()
    return total



def chang_address(driver,num_list):
    driver.execute_script("jQuery('#qy_reg_addr_sb').trigger('click')")
    time.sleep(0.2)
    driver.find_element_by_xpath('//div[@class="aui_state_box"]//ul[@class="clearfix"]/li[{num}]/a'.format(num=num_list[0])).click()
    driver.execute_script('save_City()')
    time.sleep(2)



def chang_zz(driver,num_list):
    time.sleep(2)
    driver.execute_script("jQuery('#apt_scope').trigger('click')")
    time.sleep(2)
    frame_id=re.findall('layui-layer-iframe\d+',driver.page_source)[0]
    driver.switch_to.frame(frame_id)
    driver.switch_to.frame("datalist")



def get_total(driver,num_list):
    try:
        total1=driver.find_element_by_xpath('//form[@class="pagingform"]/input[@name="$total"]').get_attribute('value')
        total1=int(total1)
    except:
        driver.find_element_by_xpath('//tr[@class="data_row"][1]')
        total1=1
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//a[@class="layui-layer-btn1"]').click()
    time.sleep(1)
    global apt_code_list
    global total_list
    global qy_region_list
    global qy_reg_addr_list
    global apt_scope_list
    global total_count_list
    global qy_type_list
    apt_code_list=[]
    total_list=[]
    qy_reg_addr_list=[]
    qy_region_list=[]
    apt_scope_list=[]
    total_count_list=[]
    qy_type_list=[]
    for i in range(1,total1+1):
        pg = i // 10 if i % 10 == 0 else i // 10 + 1
        chang_zz(driver,num_list=num_list)
        current_page=driver.find_element_by_xpath('//div[@class="quotes"]/a[@class="active"]').text

        if int(current_page) != pg:

            try:
                driver.find_element_by_xpath('//a[@class="dotted"]')
                mark=1
            except:
                driver.find_element_by_xpath('//tr[@class="data_row"][1]')
                mark=0
            if mark == 1:
                while True:
                    cmin_page=driver.find_element_by_xpath('//a[@class="dotted"][last()]/preceding-sibling::a[1]').text
                    cmax_page=driver.find_element_by_xpath('//a[@class="dotted"][last()]/following-sibling::a[1]').text

                    if int(cmin_page) < pg and int(cmax_page) > pg:
                        driver.find_element_by_xpath('//a[@class="dotted"][last()]/preceding-sibling::a[1]').click()
                        time.sleep(2)
                    else:
                        break

            driver.find_element_by_xpath('//div[@class="quotes"]/a[@dt=%s]'%pg).click()
            time.sleep(2)

        driver.find_element_by_xpath('//tr[@class="data_row"][{i}]//input/following-sibling::ins'.format(i=i%10 if i%10 else 10)).click()
        time.sleep(1)
        driver.switch_to.default_content()

        time.sleep(1)
        driver.find_element_by_xpath('//a[@class="layui-layer-btn0"]').click()
        time.sleep(2)


        driver.find_element_by_xpath('//input[@class="query_submit"]').click()
        csxx = driver.find_element_by_xpath('(//div[@class="clearfix"])[last()]/script').get_attribute('textContent')
        apt_code=re.findall('"apt_code":\["(.*?)"\],',csxx)[0]
        total2=int(re.findall('"\$total":(.*?),',csxx)[0])
        total=total2//15 if total2 % 15 == 0 else total2//15+1
        if total == 0:
            total=1
        qy_reg_addr=re.findall('"qy_reg_addr":\["(.*?)"\],',csxx)[0]
        qy_region=re.findall('"qy_region":\["(.*?)"\],',csxx)[0]
        apt_scope=re.findall('"apt_scope":\["(.*?)"\]',csxx)[0]
        qy_type=''
        apt_code_list.append(apt_code)
        total_list.append(total)
        qy_reg_addr_list.append(qy_reg_addr)
        qy_region_list.append(qy_region)
        apt_scope_list.append(apt_scope)
        total_count_list.append(total2)
        qy_type_list.append(qy_type)

    # print(apt_code_list)
    # print(total_list)
    # print(qy_reg_addr_list)
    # print(qy_region_list)
    # print(apt_scope_list)
    # print(total_count_list)
    # print(qy_type_list)


def chang_zz_1(driver,num_list):
    time.sleep(2)
    driver.find_element_by_xpath('//span[@class="dropdown-toggle"]').click()
    time.sleep(0.1)
    driver.find_element_by_xpath('//ul[@class="dropdown-menu"]/li[%s]/a'%(int(num_list[1])+2)).click()
    time.sleep(0.1)
    driver.find_element_by_xpath('//input[@class="query_submit"]').click()
    time.sleep(2)
    total1 = driver.find_element_by_xpath('//form[@class="pagingform"]/input[@name="$total"]').get_attribute('value')
    total1 = int(total1)
    return total1

def get_total_1(driver,num_list):
    global apt_code_list
    global total_list
    global qy_region_list
    global qy_reg_addr_list
    global apt_scope_list
    global total_count_list
    global qy_type_list
    apt_code_list = []
    total_list = []
    qy_reg_addr_list = []
    qy_region_list = []
    apt_scope_list = []
    total_count_list = []
    qy_type_list=[]

    csxx = driver.find_element_by_xpath('(//div[@class="clearfix"])[last()]/script').get_attribute('textContent')

    total2 = int(re.findall('"\$total":(.*?),', csxx)[0])
    total = total2 // 15 if total2 % 15 == 0 else total2 // 15 + 1
    if total == 0:
        total = 1

    qy_reg_addr=re.findall('qy_reg_addr":\["(.*?)"\],',csxx)[0]
    qy_region=re.findall('"qy_region":\["(.*?)"\],',csxx)[0]
    qy_type=re.findall('"qy_type":\["(.*?)"\],',csxx)[0]
    apt_code=''
    apt_scope=''
    apt_code_list.append(apt_code)
    total_list.append(total)
    qy_reg_addr_list.append(qy_reg_addr)
    qy_region_list.append(qy_region)
    apt_scope_list.append(apt_scope)
    total_count_list.append(total2)
    qy_type_list.append(qy_type)




def outer(f,num_list):
    def inner(*args):
        driver=args[0]
        locator = (By.XPATH, '(//td[@class="text-left primary"])[1]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath('//div[@class="plr"]//i[2]').click()
        chang_address(driver, num_list)
        total=chang_zz_1(driver,num_list)
        # chang_zz(driver, num_list)
        # get_total(driver,num_list)
        if total > 450:
            chang_zz(driver,num_list)
            get_total(driver,num_list)
        else:
            get_total_1(driver,num_list)

        return f(*args)
    return inner



def get_data():
    data = []

    zztype1 = OrderedDict([("勘察企业", "1"), ("设计企业", "2"), ("建筑业企业", "3"),("监理企业", "4"),
                           ("招标代理机构", "5"),("设计与施工一体化企业", "6"),("造价咨询企业", "7")])

    adtype1 = OrderedDict([('北京','1'),("天津", "2"), ("河北", "3"), ("山西", "4"), ("内蒙古", "5"),
                          ('辽宁','6'),('吉林','7'),('黑龙江','8'),('上海','9'),('江苏','10'),
                          ('浙江','11'),('安徽','12'),('福建','13'),('江西','14'),('山东','15'),
                          ('河南','16'),('湖北','17'),('湖南','18'),('广东','19'),('广西','20'),
                           ('海南', '21'), ('重庆', '22'), ('四川', '23'), ('贵州', '24'), ('云南', '25'),
                           ('西藏', '26'), ('陕西', '27'), ('甘肃', '28'), ('青海', '29'), ('宁夏', '30'),('新疆','31')])


    for w1 in adtype1.keys():
        for w2 in zztype1.keys():
            href = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"
            tmp = ["qyxx_diqu%s_zz%s_gg" % (adtype1[w1],zztype1[w2]), href, ["credit_code",'name','href', 'juridical_person', 'address', 'info'],
                   f1, outer(f2,[adtype1[w1],zztype1[w2]])]
            data.append(tmp)

    data1 = data.copy()

    return data1

# data=get_data()


data=[

    ["qq","http://jzsc.mohurd.gov.cn/dataservice/query/comp/list",
     ["credit_code","name","href","juridical_person","address",'info'],f1,outer(f2,[1,2])],

]


def work(conp,**args):
    est_meta(conp,data=data,**args)



if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","lch","qiyexinxi"]

    work(conp=conp,headless=False,num=3)