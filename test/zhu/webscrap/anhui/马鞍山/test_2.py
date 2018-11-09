import re
import time
import pandas as pd
# from selenium import webdriver
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#初始化
driver=webdriver.Chrome()
driver.get('http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001001/')

#第一个等待
locator=(By.XPATH,'(//td[@class="TDStyle"])[1]')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
html=driver.page_source
soup=BeautifulSoup(html,'lxml')
total=soup.find_all('font',class_="MoreinfoColor")
print(len(total))



def f1(driver, num):

    locator = (By.XPATH, '(//font[@class="MoreinfoColor"])[{}]'.format(num))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

    locator = (By.XPATH, '(//tr[@class="TDStylemore"])[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    driver.find_element_by_link_text('更多信息').click()

    locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page_num=driver.find_element_by_xpath('//div[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text

    data_list = []
    for i in range(1,int(page_num) + 1):

        df = f1_data(driver, i)
        data_list.append(df)

    data = []
    for i in data_list:
        for j in i:
            data.append(j)
    df = pd.DataFrame(data=data)
    print(df)
    return df

def f1_data(driver,page):

    if page==1:

        locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    else:
        val = driver.find_element_by_xpath('//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a').text

        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(page))

        locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('table', id='MoreInfoList1_DataGrid1')
    trs = div.find_all('tr', valign='top')

    for tr in trs:
        tds = tr.find_all('td')
        href = tds[1].a['href']
        name = tds[1].a['title']
        ggstart_time = tds[2].get_text().strip()

        if 'http' in href:
            href = href
        else:
            href = 'http://zbcg.mas.gov.cn' + href
        tmp = [name, ggstart_time, href]
        print(tmp)
        data.append(tmp)

    return data

f1(driver,2)


driver.quit()

