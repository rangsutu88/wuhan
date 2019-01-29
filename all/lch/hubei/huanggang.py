import time

import pandas as pd
import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from zhulong.util.etl import est_meta, est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='huanggang'


def f1(driver,num):
    locator = (By.XPATH, '//tr[@class="tr_main_value_odd"][1]/td[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    cnum = int(re.findall("&currpage=(\d+)&", url)[0])

    if num != cnum:
        s = "&currpage=%d&" % (num)

        url_ = re.sub("&currpage=\d+&", s, url)

        val = driver.find_element_by_xpath('//tr[@class="tr_main_value_odd"][1]/td[1]/a').get_attribute('href').rsplit(
            '/', maxsplit=1)[1]

        driver.get(url_)

        locator = (By.XPATH, '//tr[@class="tr_main_value_odd"][1]/td[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    ht = driver.page_source
    soup = BeautifulSoup(ht, 'html.parser')
    trs = soup.find_all('tr', class_=re.compile('tr_main_value_(odd|even)'))

    data = []
    for li in trs:
        name = li.find('td', align="left").a['mc']
        href = li.find('td', align="left").a['href']
        ggstart_time = li.find('td', align="left").a['rq']

        if 'http' in href:
            href = href
        else:
            href = 'http://xxgk.hg.gov.cn' + href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//tr[@class="tr_main_value_odd"][1]/td[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    total = driver.find_element_by_xpath('//table[@class="tb_title"]/tbody/tr/td[1]').text
    total = re.findall('记录.*共(.+?)页', total)[0].strip()
    total=int(total)

    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="content"]')

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
    div = soup.find('div',class_="content")
    return div




data=[

    ["zfcg_zhaobiao_gg","http://xxgk.hg.gov.cn/xxgk/jcms_files/jcms1/web1/site/zfxxgk/search.jsp?showsub=1&orderbysub=0&cid=49&vc_title=&vc_number=&currpage=1&binlay=&c_issuetime=&cid=49&jdid=1&divid=zupei_div&vc_title=&vc_number=&c_issuetime=&vc_keyword=&vc_abs=&vc_ztfl=&vc_service=&c_createtime=",["name","ggstart_time","href",'info'],f1,f2],
    ["zfcg_zhongbiao_gg","http://xxgk.hg.gov.cn/xxgk/jcms_files/jcms1/web1/site/zfxxgk/search.jsp?showsub=1&orderbysub=0&cid=50&vc_title=&vc_number=&currpage=1&binlay=&c_issuetime=&cid=50&jdid=1&divid=zupei_div&vc_title=&vc_number=&c_issuetime=&vc_keyword=&vc_abs=&vc_ztfl=&vc_service=&c_createtime=",["name","ggstart_time","href",'info'],f1,f2],

]

def work(conp,**args):
    est_meta(conp,data=data,diqu="湖北省黄冈市",**args)
    est_html(conp,f=f3,**args)



if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","lch","hubei_huanggang"]

    work(conp=conp)