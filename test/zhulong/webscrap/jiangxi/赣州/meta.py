import time

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


from  lmfscrap import web

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://www.gzzbtbzx.com/more.asp?id=5&city=1"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
def general_template(tb,url,col,conp):

    m=web()
    setting={
    "url":url,
    "f1":f1,
    "f2":f2,
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":1,
    # 'total':2


    }
    m=web()
    m.write(**setting)


def f1(driver,num):
    mark_url=driver.current_url
    if 'id' in mark_url:
        locator=(By.XPATH,'//td[@bgcolor="#DFDFDF"]/table[3]/tbody/tr/td/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        mark = re.findall(r'(id=\d+)', mark_url)[0]
        mark_2=re.findall(r'(city=\d+)',mark_url)[0]
        r_url = f3(mark,mark_2, num)

        val = driver.find_element_by_xpath('//td[@bgcolor="#DFDFDF"]/table[3]/tbody/tr/td/a').text

        driver.get(r_url)

        try:
            locator = (By.XPATH, '//td[@bgcolor="#DFDFDF"]/table[3]/tbody/tr/td/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(1)


        main_url = driver.current_url
        if 'id' in main_url:
            df=parse_1(driver)
        elif 'dq' in main_url:
            df=parse_2(driver)

        return df

    elif 'dq' in mark_url:
        locator = (By.XPATH, "//td[@bgcolor='#DFDFDF']/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        mark = re.findall(r'(dq=\d+)', mark_url)[0]
        mark_2 = re.findall(r'(dq=\d+)', mark_url)[0]
        r_url=f3(mark,mark_2,num)

        val = driver.find_element_by_xpath("//td[@bgcolor='#DFDFDF']/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a").text
        driver.get(r_url)
        try:
            locator = (By.XPATH,
             '//td[@bgcolor="#DFDFDF"]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(1)

        main_url = driver.current_url

        if 'id' in main_url:
            df=parse_1(driver)
        elif 'dq' in main_url:
            df=parse_2(driver)

        return df


def parse_1(driver):
    main_url = driver.current_url

    # print('----1111------', main_url)
    main_url = main_url.rsplit('/', maxsplit=1)[0]
    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find('td', attrs={'bgcolor': '#DFDFDF'})
    tables = content.find_all('table')
    for i in range(2, len(tables) - 1):
        table = tables[i]
        tr = table.find('tr')
        tds = tr.find_all('td')
        href = tds[0].a['href']
        if 'http' in href:
            href = href
        else:
            href = main_url + '/' + href
        name = tds[0].a.get_text()
        ggstart_time = tds[1].get_text()
        click_num = tds[2].get_text()
        tmp = [name, ggstart_time, click_num, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df
def parse_2(driver):
    main_url = driver.current_url

    # print('----2222----------------------------------------------', main_url)
    data = []
    main_url = main_url.rsplit('/', maxsplit=1)[0]

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find('td', attrs={'bgcolor': '#DFDFDF'})
    table = content.find_all('table')
    table = table[1]
    trss = table.find('table').find('table')
    trs = trss.find_all('tr')

    for i in range(3, len(trs), 2):
        tr = trs[i]
        tds = tr.find_all('td')
        href = tds[0].a['href']
        if 'http' in href:
            href = href
        else:
            href = main_url + '/' + href
        name = tds[0].a.get_text()
        ggstart_time = tds[2].get_text()
        click_num = tds[4].get_text()
        tmp = [ name, ggstart_time, click_num,href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df


def f3(mark,mark_2,num):
    main_url='http://www.gzzbtbzx.com/more.asp?{id}&{city}&page={num}'
    list_=[]
    if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
        #gcjs_zhaobiao
        list_=[276,36,125,108,91,47,42,42,55,71,37,54,61,33,46,109,40,77,50]
    elif mark == 'id=13':
        #gcjs_zhongbiaohx

        list_=[248,32,70,63,65,39,32,33,68,52,28,62,42,95,51,77,28,33,41]
    elif mark == 'id=41':

        list_=[248, 32, 70, 57, 30, 22, 25, 24, 39, 27, 21, 24, 48, 36, 35, 55, 12, 20, 41]
    elif mark=='id=2':

        list_=[95,65,11,99,24,114,14,18,11,27,13,49,28,153,108,71,4,18,28,10]
    elif mark=='id=3':

        list_=[70,29,7,49,13,89,6,10,5,12,5,17,12,121,40,25,2,10,18,5]
    elif mark=='id=5':

        list_=[91,22,1,1,1,0,1,0,0,1,0,1,2,0,1,0,0,0,8,1]


    if num <= list_[0]:
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:

            url='http://www.gzzbtbzx.com/more.asp?id=12&city=1&page={num}'.format(num=num)
        elif mark=='id=41':
            mark_2 = 'city=1'
            url=main_url.format(id=mark,city=mark_2,num=num)


        else:
            mark_2 = 'city=1'
            url = main_url.format(id=mark, city=mark_2, num=num)

    elif list_[0] < num <=sum(list_[:2]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=20&cut=&page={}".format(num-list_[0])


        else:
            mark_2 = 'city=20'
            url = main_url.format(id=mark, city=mark_2,num=num-list_[0])

    elif sum(list_[:2]) < num <=sum(list_[:3]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=2&cut=&page={}".format(num-sum(list_[:2]))


        else:
            mark_2 = 'city=2'
            url = main_url.format(id=mark, city=mark_2, num=num-sum(list_[:2]))

    elif sum(list_[:3]) < num <= sum(list_[:4]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=10&cut=&page={}".format(num-sum(list_[:3]))
        else:
            mark_2 = 'city=10'
            url = main_url.format(id=mark, city=mark_2, num=num-sum(list_[:3]))

    elif sum(list_[:4]) < num <= sum(list_[:5]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=9&cut=&page={}".format(num-sum(list_[:4]))
        else:
            mark_2 = 'city=9'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:4]))

    elif sum(list_[:5]) < num <= sum(list_[:6]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=4&cut=&page={}".format(num-sum(list_[:5]))
        else:
            mark_2 = 'city=4'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:5]))

    elif sum(list_[:6]) < num <= sum(list_[:7]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=11&cut=&page={}".format(num-sum(list_[:6]))
        else:
            mark_2 = 'city=11'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:6]))

    elif sum(list_[:7]) < num <= sum(list_[:8]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=7&cut=&page={}".format(num-sum(list_[:7]))
        else:
            mark_2 = 'city=7'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:7]))

    elif sum(list_[:8]) < num <= sum(list_[:9]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=11&cut=&page={}".format(num-sum(list_[:8]))
        else:

            mark_2 = 'city=13'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:8]))

    elif sum(list_[:9]) < num <= sum(list_[:10]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=6&cut=&page={}".format(num-sum(list_[:9]))
        else:

            mark_2 = 'city=6'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:9]))

    elif sum(list_[:10]) < num <= sum(list_[:11]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=15&cut=&page={}".format(num-sum(list_[:10]))
        else:
            mark_2 = 'city=15'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:10]))

    elif sum(list_[:11]) < num <= sum(list_[:12]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=16&cut=&page={}".format(num-sum(list_[:11]))
        else:
            mark_2 = 'city=16'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:11]))

    elif sum(list_[:12]) < num <= sum(list_[:13]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=17&cut=&page={}".format(num-sum(list_[:12]))
        else:
            mark_2 = 'city=17'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:12]))

    elif sum(list_[:13]) < num <= sum(list_[:14]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=5&cut=&page={}".format(num-sum(list_[:13]))
        else:
            mark_2 = 'city=5'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:13]))

    elif sum(list_[:14]) < num <= sum(list_[:15]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url = "http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=3&cut=&page={}".format(num - sum(list_[:14]))
        else:
            mark_2 = 'city=3'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:14]))

    elif sum(list_[:15]) < num <= sum(list_[:16]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=12&cut=&page={}".format(num-sum(list_[:15]))
        else:
            mark_2 = 'city=12'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:15]))

    elif sum(list_[:16]) < num <= sum(list_[:17]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=18&cut=&page={}".format(num-sum(list_[:16]))
        else:
            mark_2 = 'city=18'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:16]))

    elif sum(list_[:17]) < num <= sum(list_[:18]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=8&cut=&page={}".format(num-sum(list_[:17]))
        else:
            mark_2 = 'city=8'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:17]))

    elif sum(list_[:18]) < num <= sum(list_[:19]):
        if mark in ['id=12','dq=20','dq=2','dq=10','dq=9','dq=4',
                'dq=11','dq=7','dq=13','dq=6','dq=15','dq=16',
                'dq=17','dq=5','dq=3','dq=12','dq=18','dq=8','dq=14']:
            url="http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=14&cut=&page={}".format(num-sum(list_[:18]))
        else:
            mark_2 = 'city=14'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:18]))
    if mark in ['id=2','id=3','id=5']:
        if sum(list_[:19]) < num <= sum(list_[:20]):
            mark_2='city=19'
            url = main_url.format(id=mark, city=mark_2, num=num - sum(list_[:19]))

    r_url=url
    return r_url

def f2(driver):
    url=driver.current_url
    mark = re.findall(r'(id=\d+&city=\d+)', url)[0]
    if mark=='id=12&city=1':
        dict_={'sbj': 276, 'zhgq': 36,'gx':125,'nk':108,'xf':91,'dy':47,
               'sy':42,'cy':42,'ay':55,'ln':71,'qn':37,'dn':54,'xg':61,
               'nd':33,'yd':46,'rj':109,'hc':40,'xw':77,'sc':50}
        #gcjs_zhaobiao
        total=sum([276,36,125,108,91,47,42,42,55,71,37,54,61,33,46,109,40,77,50])

    elif mark=='id=13&city=1':
        dict_ = {'sbj': 248, 'zhgq': 32, 'gx': 70, 'nk':63 , 'xf': 65, 'dy': 39,
                 'sy': 32, 'cy': 33, 'ay': 68, 'ln': 52, 'qn': 28, 'dn': 62, 'xg': 42,
                 'nd': 95, 'yd': 51, 'rj': 77, 'hc': 28, 'xw': 33, 'sc': 41}
        #gcjs_zhongbiao
        total = sum([248,32,70,63,65,39,32,33,68,52,28,62,42,95,51,77,28,33,41])

    elif mark=='id=41&city=1':
        dict_ = {'sbj': 248, 'zhgq': 32, 'gx': 70, 'nk': 57, 'xf': 30, 'dy': 22,
                 'sy': 25, 'cy': 24, 'ay': 39, 'ln': 27, 'qn': 21, 'dn': 24, 'xg': 48,
                 'nd': 36, 'yd': 35, 'rj': 55, 'hc': 12, 'xw': 20, 'sc': 41}
        #gcjs_dayi
        total = sum([248, 32, 70, 57, 30, 22, 25, 24, 39, 27, 21, 24, 48, 36, 35, 55, 12, 20, 41])
    elif mark=='id=2&city=1':
        dict_ = {'sbj': 95, 'zhgq': 65, 'gx': 11, 'nk': 99, 'xf': 24, 'dy': 114,
                 'sy': 14, 'cy': 18, 'ay': 11, 'ln': 27, 'qn': 13, 'dn': 49, 'xg': 28,
                 'nd': 153, 'yd': 108, 'rj': 71, 'hc': 4, 'xw': 18, 'sc': 28,'kfq':10}
        # zfcg_zhaobiao
        total = sum([95,65,11,99,24,114,14,18,11,27,13,49,28,153,108,71,4,18,28,10])

    elif mark=='id=3&city=1':
        dict_ = {'sbj': 70, 'zhgq': 29, 'gx': 7, 'nk': 49, 'xf': 13, 'dy': 89,
                 'sy': 6, 'cy': 10, 'ay': 5, 'ln': 12, 'qn': 5, 'dn': 17, 'xg': 12,
                 'nd': 121, 'yd': 40, 'rj': 25, 'hc': 2, 'xw': 10, 'sc': 18, 'kfq': 5}
        # zfcg_zhongbiao
        total = sum([70,29,7,49,13,89,6,10,5,12,5,17,12,121,40,25,2,10,18,5])

    elif mark=='id=5&city=1':
        dict_ = {'sbj': 91, 'zhgq': 22, 'gx': 1, 'nk': 1, 'xf': 1, 'dy': 0,
                 'sy': 1, 'cy': 0, 'ay': 0, 'ln': 1, 'qn': 0, 'dn': 1, 'xg': 2,
                 'nd': 0, 'yd': 1, 'rj': 0, 'hc': 0, 'xw': 0, 'sc': 8, 'kfq': 1}
        # gcjs_bumen
        total = sum([91,22,1,1,1,0,1,0,0,1,0,1,2,0,1,0,0,0,8,1])
    total=int(total)
    return total

def work(conp,i=-1):
    data=[
        #
        ["gcjs_zhaobiao_gg","http://www.gzzbtbzx.com/more.asp?id=12&city=1",["name","ggstart_time","click_num","href"]],
        ["gcjs_zhongbiaohx_gg","http://www.gzzbtbzx.com/more.asp?id=13&city=1",["name","ggstart_time","click_num","href"]],
        ["gcjs_dayibucong_gg","http://www.gzzbtbzx.com/more.asp?id=41&city=1",["name","ggstart_time","click_num","href"]],
        #
        #
        ["zfcg_zhaobiao_gg","http://www.gzzbtbzx.com/more.asp?id=2&city=1",["name","ggstart_time","click_num","href"]],
        ["zfcg_bumen_gg","http://www.gzzbtbzx.com/more.asp?id=5&city=1",["name","ggstart_time","click_num","href"]],
        ["zfcg_zhongbiao_gg","http://www.gzzbtbzx.com/more.asp?id=3&city=1",["name","ggstart_time","click_num","href"]],

    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
# conp=["testor","zhulong","192.168.3.171","test","lch"]
# conp=["testor","zhulong","192.168.3.171","test","public"]
conp=["postgres","since2015","192.168.3.171","jiangxi","ganzhou"]

work(conp=conp)