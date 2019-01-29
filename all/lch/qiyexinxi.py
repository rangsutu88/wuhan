import random
import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import requests
import json
from fake_useragent import UserAgent

from zhulong.util.etl import est_tbs, est_meta, est_html, gg_existed, est_gg

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]

#
url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"
driver = webdriver.Chrome()
driver.minimize_window()
driver.get(url)

_name_ = ''


def f1(driver, num):
    locator = (By.XPATH, '(//td[@class="text-left primary"])[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    ua = UserAgent()
    cookies = driver.get_cookies()
    COOKIES = {}
    for cookie in cookies:
        COOKIES[cookie['name']] = cookie['value']
    print(COOKIES)
    form_data = {

        "apt_code": "D101T",
        "qy_fr_name": "",
        "$total": 16,
        "qy_reg_addr": "江西省",
        "qy_code": "",
        "qy_name": "",
        "$pgsz": 15,
        "apt_certno": "",
        "qy_region": 360000,
        "$reload": 0,
        "qy_type": "",
        "$pg": 2,
        "qy_gljg": "",
        "apt_scope": "建筑工程施工总承包特级",

    }
    headers = {

        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "jzsc.mohurd.gov.cn",
        "Origin": "http://jzsc.mohurd.gov.cn",
        "Referer": "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    time.sleep(random.random())
    req = requests.post(url, data=form_data, headers=headers, cookies=COOKIES, timeout=20)

    if req.status_code != 200:
        print(req.text)
        raise ValueError('Error response status_code %s' % req.status_code)
    ht = req.text
    soup = BeautifulSoup(ht, 'lxml')
    trs = soup.find('tbody', class_="cursorDefault").find_all('tr', recursive=False)

    data = []
    for tr in trs:
        tds = tr.find_all('td')
        credit_code = tds[1].get_text().strip()
        name = tds[2].a.get_text().strip()
        href = tds[2].a['href']
        if 'http' in href:
            href = href
        else:
            href = "http://jzsc.mohurd.gov.cn" + href
        juridical_person = tds[3].get_text().strip()
        address = tds[4].get_text().strip()
        tmp = [credit_code, name, href, juridical_person, address]
        data.append(tmp)
    print(data)
    df = pd.DataFrame(data=data)
    df['info'] = None
    return df


def f2(driver):
    locator = (By.XPATH, '(//td[@class="text-left primary"])[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    total = int(
        driver.find_element_by_xpath('//form[@class="pagingform"]/input[@name="$total"]').get_attribute('value'))
    total = total // 15 if total % 15 == 0 else total // 15 + 1

    driver.quit()
    return total


def chang_address(driver, num_list):
    driver.execute_script("jQuery('#qy_reg_addr_sb').trigger('click')")
    time.sleep(0.2)
    driver.find_element_by_xpath(
        '//div[@class="aui_state_box"]//ul[@class="clearfix"]/li[{num}]/a'.format(num=num_list[0])).click()
    driver.execute_script('save_City()')
    time.sleep(2)


def chang_zz(driver, num_list):
    time.sleep(2)
    driver.execute_script("jQuery('#apt_scope').trigger('click')")
    time.sleep(2)
    frame_id = re.findall('layui-layer-iframe\d+', driver.page_source)[0]
    driver.switch_to.frame(frame_id)
    Select(driver.find_element_by_xpath('//select[@id="apt_root"]')).select_by_index(num_list[1])
    time.sleep(2)
    driver.switch_to.frame("datalist")


def get_total(driver, num_list):
    total = driver.find_element_by_xpath('//form[@class="pagingform"]/input[@name="$total"]').get_attribute('value')
    total = int(total)
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//a[@class="layui-layer-btn1"]').click()
    time.sleep(1)
    global apt_code_list
    global total_list
    global qy_region_list
    global qy_reg_addr_list
    global apt_scope_list
    apt_code_list = []
    total_list = []
    qy_reg_addr_list = []
    qy_region_list = []
    apt_scope_list = []
    for i in range(1, total + 1):
        chang_zz(driver, num_list=num_list)
        canshu1 = driver.find_element_by_xpath('(//div[@class="clearfix"])[last()]/script').get_attribute('textContent')
        apt_root=re.findall('"apt_root":\[".*?"\]',canshu1)[0]
        total1=re.findall('"\$total":.*?,',canshu1)[0]
        pg=i // 10 if i % 10==0 else i // 10 + 1
        url="http://jzsc.mohurd.gov.cn/asite/qualapt/aptData"
        headers = {

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "jzsc.mohurd.gov.cn",
            "Origin": "http://jzsc.mohurd.gov.cn",
            "Referer": "http://jzsc.mohurd.gov.cn/asite/qualapt/aptData",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        form_data={

            "apt_root": apt_root,
            "$total": total1,
            "$reload": 0,
            "apt_type":"",
            "$pg":pg,
            "$pgsz": 10,

        }
        cookies = driver.get_cookies()
        COOKIES = {}
        for cookie in cookies:
            COOKIES[cookie['name']] = cookie['value']

        req=requests.post(url,data=form_data,headers=headers,cookies=COOKIES)

        if req.status_code != 200 :
            raise ValueError('Error response status_code %s'%req.status_code)
        content=req.text
        canshu2=re.findall('')



        # driver.find_element_by_xpath('//tr[@class="data_row"][{i}]//input/following-sibling::ins'.format(i=i)).click()
        # time.sleep(1)
        # driver.switch_to.default_content()
        #
        # time.sleep(2)
        # driver.find_element_by_xpath('//a[@class="layui-layer-btn0"]').click()
        # time.sleep(2)
        #
        # driver.find_element_by_xpath('//input[@class="query_submit"]').click()
        # canshu2 = driver.find_element_by_xpath('(//div[@class="clearfix"])[last()]/script').get_attribute('textContent')
        canshu2=''

        apt_code = re.findall('"apt_code":\[".*?"\],', canshu2)[0]
        total = re.findall('"\$total":.*?,', canshu2)[0]
        qy_reg_addr = re.findall('"qy_reg_addr":\[".*?"\],', canshu2)[0]
        qy_region = re.findall('"qy_region":\[".*?"\],', canshu2)[0]
        apt_scope = re.findall('"apt_scope":\[".*?"\]', canshu2)[0]
        apt_code_list.append(apt_code)
        total_list.append(total)
        qy_reg_addr_list.append(qy_reg_addr)
        qy_region_list.append(qy_region)
        apt_scope_list.append(apt_scope)

    print(apt_code_list)
    print(total_list)
    print(qy_reg_addr_list)
    print(qy_region_list)
    print(apt_scope_list)


def outer(f, num_list):
    def inner(*args):
        driver = args[0]
        locator = (By.XPATH, '(//td[@class="text-left primary"])[1]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        chang_address(driver, num_list)
        driver.find_element_by_xpath('//div[@class="plr"]//i[2]').click()
        chang_zz(driver, num_list)
        get_total(driver, num_list)

        return f(*args)

    return inner


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="cont_t"]')

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
    div = soup.find('div', class_="cont_t").parent

    return div


data = [
    #
    ["qiyexingxi", "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list",
     ["credit_code", 'name', 'href' 'juridical_person', 'address', 'info'], f1, outer(f2, [2, 2])],

]


def work(conp, **args):
    est_meta(conp, data=data, **args)
    # est_html(conp,f=f3,**args)


if __name__ == '__main__':
    conp = ["postgres", "since2015", "192.168.3.171", "test", "lch"]

    work(conp=conp, num=1, headless=False)