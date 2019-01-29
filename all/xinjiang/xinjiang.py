import json
import time

import pandas as pd
import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lch.zhulong import est_meta, est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hefei.gov.cn/jyxx/002001/002001002/moreinfo_jyxx.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


_name_ = 'xinjiang'


def f1(driver, num):
    driver.refresh()
    try:
        locator = (By.XPATH, '(//table[@class="tab top10"][1]//table[@class="top10"]//table)[1]//tr[1]//a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        driver.refresh()
        locator = (By.XPATH, '(//table[@class="tab top10"][1]//table[@class="top10"]//table)[1]//tr[1]//a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    url = driver.current_url

    cnum = re.findall('Paging=(\d+)', url)[0]

    main_url = url.rsplit('=', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath(
            '(//table[@class="tab top10"][1]//table[@class="top10"]//table)[1]//tr[1]//a').get_attribute('href').rsplit(
            '/', maxsplit=1)[1]

        url = main_url + '=%s' % num

        driver.get(url)
        time.sleep(0.1)
        driver.refresh()
        try:
            locator = (By.XPATH,
                   '(//table[@class="tab top10"][1]//table[@class="top10"]//table)[1]//tr[1]//a[not(contains(@href,"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:

            driver.refresh()
            locator = (By.XPATH,
                       '(//table[@class="tab top10"][1]//table[@class="top10"]//table)[1]//tr[1]//a[not(contains(@href,"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            ccnum=driver.find_element_by_xpath('//td[@class="yahei redfont"]').text.strip()
            if int(ccnum) != num:
                raise ValueError


    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.find_all('tr', height='30')

    for li in lis:
        href = li.find('td', align='left').a['href']
        name = li.find('td', align='left').a['title']
        try:
            bingtuan = li.find('td', align='left').a.font.get_text().strip()
            bingtuan = re.findall(r'\[(.+)\]', bingtuan)[0]
        except:
            bingtuan=None

        ggstart_time = li.find('td', width='90').get_text().strip(']').strip('[')
        info={'bingtuan':bingtuan}
        info=json.dumps(info,ensure_ascii=False)
        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.xjbt.gov.cn' + href

        tmp = [name, ggstart_time,href,info]
        data.append(tmp)
    df = pd.DataFrame(data=data)

    return df


def f2(driver):
    locator = (By.XPATH, '(//table[@class="tab top10"][1]//table[@class="top10"]//table)[1]//tr[1]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//td[@class="huifont"]').text

    total = re.findall('/(\d+)', page)[0]
    total = int(total)

    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//table[@id="tblInfo"]')

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

    div = soup.find('table',id="tblInfo")

    return div


data = [

    ["gcjs_zhaobiao_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004001/004001002/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],
    ["gcjs_biangengdayi_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004001/004001003/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],
    ["gcjs_zhongbiaohx_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004001/004001004/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],
    ["gcjs_zhongbiao_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004001/004001005/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],
    ["gcjs_zishenjieguo_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004001/004001006/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],
    ["gcjs_biangeng_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004001/004001007/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],

    ["zfcg_zhaobiao_danyilaiyuan_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004002/004002006/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],
    ["zfcg_zhaobiao_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004002/004002002/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],
    ["zfcg_biangeng_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004002/004002003/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],
    ["zfcg_dayichengqing_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004002/004002004/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],
    ["zfcg_zhongbiao_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004002/004002005/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],

    ##包含招标,变更
    ["qsydw_zhao_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004005/004005001/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],
    ##包含中标,流标
    ["qsydw_zhong_gg", "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004005/004005002/?Paging=1", ['name', 'ggstart_time', 'href', 'info'],f1, f2],

]


def work(conp, **args):
    est_meta(conp, data=data, diqu="新疆省新疆", **args)
    est_html(conp, f=f3, **args)

if __name__ == '__main__':
    conp = ["postgres", "since2015", "192.168.3.171", "xinjiang", "xinjiang"]

    work(conp=conp,pageloadtimeout=60)