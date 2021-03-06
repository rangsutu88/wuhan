import re
import time

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
driver.get('http://ggzyjy.xuancheng.gov.cn/XCTPFront/jsgc/011001/011001001/')

#第一个等待
locator=(By.XPATH,'//tr[@class="trfont"][1]/td[2]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))


cnum=driver.find_element_by_xpath('//td[@class="huifont"]').text
cnum=re.findall('(\d+)/',cnum)[0]
print(cnum)
#第二个等待
val=driver.find_element_by_xpath('//tr[@class="trfont"][1]/td[2]/a').text
print(val)
num=2

# driver.get(url)
#翻页


driver.execute_script("window.location.href='./?Paging={}'".format(num))


#第二个等待

locator = (By.XPATH, '//tr[@class="trfont"][1]/td[2]/a[not(contains(string(),"{}"))]'.format(val))
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
total=driver.find_element_by_xpath('//td[@class="huifont"]').text
total=re.findall('\/(\d+)',total)[0]

total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
trs=soup.find_all('tr',class_="trfont")

for tr in trs:
    href=tr.find('td',align='left').a['href']
    name=tr.find('td',align='left').a['title']

    ggstart_time=tr.find('td',align='right').get_text()
    if 'http' in href:
        href=href
    else:
        href='http://ggzyjy.xuancheng.gov.cn'+href

    tmp = [ name, ggstart_time, href]
    print(tmp)

driver.quit()

