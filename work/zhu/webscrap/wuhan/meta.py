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

from lmfscrap import web

# __conp=["postgres","since2015","192.168.3.171","hunan","zhuzhou"]


# url = "http://www.whzbtb.cn/V2PRTS/TendererNoticeInfoListInit.do"
# driver=webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
# driver = webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



def f1(driver, num):
    locator = (By.CLASS_NAME, "datagrid-td-rownumber")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    print('正在爬取第{}页数据'.format(num))
    driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[7]/input').clear()
    driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[7]/input').send_keys(
        num, Keys.ENTER)
    WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="datagrid-row-r1-1-9"]/td[1]/div'), str(num * 10)))
    page=driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    soup = BeautifulSoup(page, 'lxml')
    tables = soup.find('div', class_='datagrid-view')
    trs = tables.find_all('tr')
    # ul=tables.find_all
    # print(int(len(trs) + 1) // 2)
    data=[]
    for i in range(1, int(len(trs) + 1) // 2):
        tmp = []
        tr = trs[i]
        a = tr.find('a')
        url = re.findall(r"'.+'", str(a))[0].strip(r"'")
        cons = tr.find_all('div')
        for j in cons:
            con = j.get_text()
            tmp.append(con)
        tr = trs[i + int(len(trs) + 1) // 2]
        cons = tr.find_all('div')
        for j in cons:
            con = j.get_text()
            tmp.append(con)
        tmp.append('http://www.whzbtb.cn/V2PRTS/' + url)
        data.append(tmp)

    df = pd.DataFrame(data=data)
    # print(data)
    return df

    # for li in lis:
    #     a = li.find("a")
    #     span = li.find("span", recursive=False)
    #     tmp = [a["title"], "http://www.zzzyjy.cn" + a["href"], span.text.strip()]
    #     data.append(tmp)
    # df = pd.DataFrame(data=data)
    # return df


def f2(driver):
    locator = (By.XPATH, '//*[@id="datagrid-row-r1-1-0"]/td[2]/div/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    time.sleep(1)
    total = driver.find_element_by_xpath("//div[@class='datagrid-pager pagination']"
                                             "/table/tbody/tr/td[8]/span").text
    total=int(re.findall('共(.+)页',total)[0])
    return total
    # else:
    #     driver.quit()
    #     return 1


def general_template(tb, url, col, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f1,
        "f2": f2,
        "tb": tb,  # 数据库名
        "col": col,  # 数据库字段名
        "conp": conp,
        "num": 2,
        'total':10

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["TendererNoticeInfoListInit", "http://www.whzbtb.cn/V2PRTS/TendererNoticeInfoListInit.do",
         ["a", "b", "c","d",'e','f','g',"h",'i','j','q']],



    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2], conp)

# conp=["testor","zhulong","192.168.3.171","test","public"]
#
# work(conp=conp,i=0)

