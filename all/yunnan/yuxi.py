import time

import pandas as pd

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from lch.zhulong import est_meta, est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='yuxi'

def f1(driver,num):
    locator = (By.XPATH, '//div[@class="news"]/table/tbody/tr[2]/td[3]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    cnum = driver.find_element_by_xpath('//a[@class="cur"]').text.strip()

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//div[@class="news"]/table/tbody/tr[2]/td[3]').text

        driver.execute_script("pagination({});return false;".format(num))

        locator = (By.XPATH, '//div[@class="news"]/table/tbody/tr[2]/td[3][not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))



    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_='news').find('table')
    trs = div.find_all('tr')

    if ("jsgcZbgg" in url) or ('cggg' in url):
        data=parse_1(trs)
    elif 'jsgcBgtz' in url:
        data=parse_2(trs)
    elif ('jsgcZbyc' in url) or ('zfcgYcgg' in url):
        data=parse_4(trs)
    else:
        data=parse_3(trs,url)

    df=pd.DataFrame(data=data)
    df['info']=None
    return df
def parse_1(trs):
    data = []
    for i in range(1, len(trs)):
        tr = trs[i]
        tds = tr.find_all('td')
        index_num = tds[1].get_text()
        href = tds[2].a['href']
        name = tds[2].a['title']
        ggstart_time = tds[3].get_text()
        ggend_time = tds[4].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://60.160.190.130:8001' + href

        tmp = [index_num, name, href, ggstart_time, ggend_time]
        data.append(tmp)
    return data

def parse_2(trs):
    data = []
    for i in range(1, len(trs)):
        tr = trs[i]
        tds = tr.find_all('td')
        index_num = tds[1].get_text()
        title = tds[2].get_text()
        href = tds[3].a['href']
        name = tds[3].a['title']
        ggstart_time = tds[4].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://60.160.190.130:8001' + href
        tmp = [index_num, title, name, href, ggstart_time]
        data.append(tmp)
    return data
def parse_3(trs,url):
    data = []
    for i in range(1, len(trs)):
        tr = trs[i]
        tds = tr.find_all('td')
        index_num = tds[1].get_text()

        href = tds[2].a['href']

        if 'jsgcZbjggs' in url:
            name = tds[2]['title']
        else:
            name=tds[2].a['title']

        ggstart_time = tds[3].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://60.160.190.130:8001' + href

        tmp = [index_num, name, href, ggstart_time]
        # print(tmp)
        data.append(tmp)

    return data

def parse_4(trs):
    data = []
    for i in range(1, len(trs)):
        tr = trs[i]
        tds = tr.find_all('td')
        index_num = tds[1].get_text()

        href = tds[2].a['href']
        name = tds[2].a['title']
        yctype = tds[3].get_text()
        ggstart_time = tds[4].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://60.160.190.130:8001' + href

        tmp = [index_num, name, href, yctype, ggstart_time]
        data.append(tmp)

    return data

def f2(driver):
    locator = (By.XPATH, '//div[@class="news"]/table/tbody/tr[2]/td[3]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//div[@class="mmggxlh"]/a[last()-1]').text
    total = int(page)
    driver.quit()
    return total

def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="con"] | //div[@class="news-layout"]')

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
    div = soup.find('div', class_='con')
    if div == None:
        div = soup.find('div', class_="news-layout")

    return div

data=[
    #
    ["gcjs_zhaobiao_gg","http://60.160.190.130:8001/jyxx/jsgcZbgg",["index_num", "name", "href", "ggstart_time", "ggend_time","info"],f1,f2],
    ["zfcg_zhaobiao_gg","http://60.160.190.130:8001/jyxx/zfcg/cggg",["index_num", "name", "href", "ggstart_time", "ggend_time","info"],f1,f2],

    ["gcjs_biangengdayi_gg","http://60.160.190.130:8001/jyxx/jsgcBgtz",["index_num", 'title',"name", "href", "ggstart_time","info"],f1,f2],

    ["gcjs_zhongbiaohx_gg","http://60.160.190.130:8001/jyxx/jsgcpbjggs",["index_num", "name", "href", "ggstart_time","info"],f1,f2],

    ["gcjs_zhongbiao_gg","http://60.160.190.130:8001/jyxx/jsgcZbjggs",["index_num", "name", "href", "ggstart_time","info"],f1,f2],

    ["gcjs_liubiao_gg","http://60.160.190.130:8001/jyxx/jsgcZbyc",["index_num", "name", "href", "yctype","ggstart_time","info"],f1,f2],
    ["zfcg_liubiao_gg","http://60.160.190.130:8001/jyxx/zfcg/zfcgYcgg",["index_num", "name", "href", "yctype","ggstart_time","info"],f1,f2],

    ["zfcg_biangengdayi_gg","http://60.160.190.130:8001/jyxx/zfcg/gzsx",["index_num", "name", "href", "ggstart_time","info"],f1,f2],
    ["zfcg_zhongbiao_gg","http://60.160.190.130:8001/jyxx/zfcg/zbjggs",["index_num", "name", "href", "ggstart_time","info"],f1,f2],


]

def work(conp,**args):
    est_meta(conp,data=data,diqu="云南省玉溪市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","yunnan","yuxi"]

    work(conp=conp,num=10)