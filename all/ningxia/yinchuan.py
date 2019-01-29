import time

import pandas as pd
import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

from lch.zhulong import est_meta, est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://www.ycsggzy.cn/morelink.html?type=12&index=0"
# driver=webdriver.Chrome()
# driver.maximize_window()
# driver.get(url)

_name_='yinchuan'

def f1(driver,num):
    # locator = (By.XPATH, '//div[@id="showline_div"]/ul/li[1]/a')
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # url=driver.current_url
    # while True:
    #     locator = (By.XPATH, '//div[@class="page"]/b')
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    #
    #     cnum = driver.find_element_by_xpath('//div[@class="page"]/b').text.strip()
    #     cnum = int(cnum)
    #     val = driver.find_element_by_xpath('//div[@id="showline_div"]/ul/li[1]/a').text
    #     if num == cnum:
    #         break
    #     if num ==1:
    #         driver.execute_script("gofirst()")
    #     else:
    #         if num > cnum:
    #             if num - cnum > TOTAL_PAGE//2 and 'type=12&index=0' not in url:
    #                 driver.execute_script('golast()')
    #             else:
    #                 driver.execute_script('gonext()')
    #         if  num < cnum:
    #             if cnum - num > TOTAL_PAGE//2:
    #                 driver.execute_script('gofirst()')
    #             else:
    #                 driver.execute_script('goprev()')
    #
    #     locator = (By.XPATH, '//div[@id="showline_div"]/ul/li[1]/a[not(contains(string(),"%s"))]' % val)
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    post_url='http://www.ycsggzy.cn/Ajax/morelink.ashx'
    mark_url=driver.current_url

    type=re.findall('type=(\d+)&',mark_url)[0]
    index=re.findall('index=(\d+)',mark_url)[0]
    from_data={
        'czlx': 'linetxt',
        'cxcs': '{type}|{index}|{num}|20'.format(type=type,index=index,num=num),
    }
    headers={
        'Referer': mark_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }

    req=requests.post(post_url,data=from_data,headers=headers)
    if int(req.status_code) == 200:
        html=req.content
    else:
        raise TimeoutError
    data = []

    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('ul')
    lis = div.find_all('li')

    for li in lis:

        href = li.a['href']
        ggstart_time = li.a.span.extract().get_text()
        name = li.a.get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://www.ycsggzy.cn/' + href

        tmp = [name, href, ggstart_time]
        data.append(tmp)

    df=pd.DataFrame(data=data)
    df['info']=None
    return df



def f2(driver):
    global TOTAL_PAGE
    TOTAL_PAGE=1
    locator = (By.XPATH, '//div[@id="showline_div"]/ul/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//a[@title="Total record"]/b').text
    total=int(page)
    TOTAL_PAGE=total

    driver.quit()
    return total

def f3(driver, url):
    driver.get(url)
    try:
        locator = (By.XPATH, '//ul[@class="a_content"]')

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
    except:
        html=driver.page_source
        if '请稍候,正在刷新' in html:
            # driver.refresh()
            # locator = (By.XPATH, '//ul[@class="a_content"]')
            # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
            return 404
        else:
            raise TimeoutError

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
    div = soup.find('ul', class_="a_content")

    return div

data=[

    #包含:变更,招标


    ######网站有十五页异常,无法爬取
    ["zfcg_zhao_gg","http://www.ycsggzy.cn/morelink.html?type=12&index=0",[ "name", "href", "ggstart_time","info"],f1,f2],

    #####以下都可以正常爬取

    ["gcjs_zhao_gg","http://www.ycsggzy.cn/morelink.html?type=12&index=1",[ "name", "href", "ggstart_time","info"],f1,f2],

    #####包含:中标,流标
    ["zfcg_zhong_gg","http://www.ycsggzy.cn/morelink.html?type=17&index=0",[ "name", "href", "ggstart_time","info"],f1,f2],
    ["gcjs_zhong_gg","http://www.ycsggzy.cn/morelink.html?type=17&index=1",[ "name", "href", "ggstart_time","info"],f1,f2],


]

def work(conp,**args):
    est_meta(conp,data=data,diqu="宁夏回族自治区银川",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","ningxia","yinchuan"]

    work(conp=conp,num=10)