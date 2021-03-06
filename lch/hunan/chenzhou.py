import datetime
import json
import random
import time

import pandas as pd

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

from zhulong.util.etl import est_meta, est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='chenzhou'


def f1(driver,num):

    ua=UserAgent()
    time.sleep(0.1)
    for i in range(1, int(len(PAGE)) + 1):
        if sum(PAGE[:i - 1]) < num <= sum(PAGE[:i]):
            num = num - sum(PAGE[:i - 1])

            headers = {
                "User-Agent": ua.chrome,
                "Referer": "http://www.ccgp-hunan.gov.cn/page/notice/more_city.jsp?noticeTypeID=prcmNotices&area_id=86",
                       }

            form_data = {
                "startDate": str(DATE[i]+datetime.timedelta(days=1)),
                "endDate": str(DATE[i - 1]),
                "page": num,
                "pageSize": 18,
                "area_id": 86,
                "areaCode": "czs",
            }

            url = "http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4WebCity.do"
            time.sleep(random.random())

            req = requests.post(url, data=form_data,headers=headers,timeout=10)
            if req.status_code != 200:
                print(req.status_code)
                raise ValueError

            response = json.loads(req.text)

            contents = response['rows']

            data_=[]
            for content in contents:

                name = content.get('NOTICE_TITLE')
                address = content.get('AREA_NAME')
                ggstart_time = content.get('NEWWORK_DATE')
                gg_type = content.get('NOTICE_NAME')
                jy_type = content.get('PRCM_MODE_NAME')
                type = content.get('NOTICE_TYPE_NAME')
                org_name = content.get('DEPT_NAME')
                href = content.get('NOTICE_ID')

                src_code = content.get('SRC_CODE')

                if int(src_code) == 1:
                    href = "http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp?noticeId=" + str(href)
                else:
                    href = "http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp?noticeId=" + str(href) + '&area_id=86'

                tmp = [name, address, ggstart_time, type, gg_type, jy_type, org_name, href]
                data_.append(tmp)

            is_useful = True
            break

    if 'is_useful' not in locals():
        print('页数不合法%d' % num)


    df=pd.DataFrame(data=data_)
    df["info"] = None
    return df


def f2(driver):
    global DATE
    global PAGE
    DATE=[]
    PAGE = []
    now_time = datetime.date.today()
    time_interval = datetime.timedelta(days=300)
    last_time = now_time - time_interval
    end_time = datetime.date(year=2015, month=1, day=1)
    date_list = []
    date_list.extend([now_time, last_time])

    while last_time > end_time:
        last_time -= time_interval
        date_list.append(last_time)
    DATE=date_list.copy()

    while len(date_list) > 1:
        form_data = {
            "startDate": str(date_list[1]+datetime.timedelta(days=1)),
            "endDate": str(date_list[0]),
            "page": 1,
            "pageSize": 18,
            "area_id": 86,
            "areaCode": "czs",
        }

        url = "http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4WebCity.do"

        req = requests.post(url, data=form_data)
        content = json.loads(req.text)

        count_num = int(content['total'])
        page_count = count_num // 18 + 1 if count_num % 18 else count_num // 18

        PAGE.append(page_count)
        date_list = date_list[1:]
    total=sum(PAGE)

    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)
    time.sleep(0.5)
    try:
        driver.switch_to.frame("content")
        mark=1
    except:
        mark=0
        pass
    if mark:
        locator = (By.XPATH, '//body')

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
    else:
        raise ValueError

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
    div = soup.find('body')
    driver.switch_to.parent_frame()

    return div



data=[

    ["zfcg_gg","http://www.ccgp-hunan.gov.cn/page/notice/more_city.jsp?noticeTypeID=prcmNotices&area_id=86",
     ["name", "address", "ggstart_time", "type", "gg_type", "jy_type", "org_name",  "href",'info'],f1,f2],

]

def work(conp,**args):
    est_meta(conp,data=data,diqu="湖南省郴州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","lch","hunan_chenzhou"]

    work(conp=conp,pageloadtimeout=120,cdc_total=20,headless=False)