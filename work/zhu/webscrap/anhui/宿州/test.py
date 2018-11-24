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
driver.get('http://www.szggzyjy.cn/szfront/jyxx/002005/002005001/')

#第一个等待
locator=(By.XPATH,'//ul[@class="ewb-lbd-items"]/li/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url

main_url=url.rsplit('=',maxsplit=1)[0]



cnum=driver.find_element_by_xpath('//td[@class="huifont"]').text
cnum=re.findall('(\d+)/',cnum)[0]
print(cnum)
#第二个等待
val=driver.find_element_by_xpath('//ul[@class="ewb-lbd-items"]/li/a').text
print(val)
num=2

# driver.get(url)
#翻页
driver.execute_script("window.location.href='./?Paging={}'".format(num))
#第二个等待
locator = (By.XPATH, '//ul[@class="ewb-lbd-items"]/li/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
total=driver.find_element_by_xpath('//td[@class="huifont"]').text
total=re.findall('\/(\d+)',total)[0]

total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('ul',class_='ewb-lbd-items')
trs=div.find_all('li')
print(len(trs))
for tr in trs:
    href=tr.a['href']
    name=tr.a['title']
    ggstart_time=tr.span.get_text()

    if 'http' in href:
        href=href
    else:
        href='http://www.szggzyjy.cn'+href

    tmp = [ name, ggstart_time, href]
    print(tmp)

driver.quit()

