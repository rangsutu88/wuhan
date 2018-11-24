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
driver.get('http://www.czggzy.gov.cn/Front_jyzx/jyxx/002008/002008001/002008001001/?Paging=1')

#第一个等待
locator=(By.XPATH,'//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url

main_url=url.rsplit('=',maxsplit=1)[0]



cnum=driver.find_element_by_xpath('//td[@class="huifont"]').text
cnum=re.findall('(\d+)/',cnum)[0]
print(cnum)
#第二个等待
val=driver.find_element_by_xpath('//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a').text
print(val)
num=2
url=main_url+'='+str(num)
# driver.get(url)
#翻页
driver.execute_script("window.location.href='./?Paging={}'".format(num))
#第二个等待
locator = (By.XPATH, '//div[@class="right-wrap-ccontent-text"]/div/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
total=driver.find_element_by_xpath('//td[@class="huifont"]').text
total=re.findall('\/(\d+)',total)[0]

total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('div',class_='right-wrap-ccontent-text')
trs=div.find_all('tr',height=25)
print(len(trs))
for tr in trs:
    href=tr.find('td',align='left').a['href']
    name=tr.find('td',align='left').a['title']
    ggstart_time=tr.find('td',align='right').get_text()

    if 'http' in href:
        href=href
    else:
        href='http://www.czggzy.gov.cn'+href

    tmp = [ name, ggstart_time, href]
    print(tmp)

driver.quit()

