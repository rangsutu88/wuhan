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

driver=webdriver.Chrome()
driver.get('http://www.jdz.gov.cn/xxgk/050014/050014004/2.html')

locator=(By.XPATH,'//*[@id="rightout"]/div[1]/ul/li[1]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# time.sleep(1)
url=driver.current_url

num=1
print(url)
url=url.rsplit('/',maxsplit=1)[0]+'/'+'{}.html'.format(num)
print(url)
val=driver.find_element_by_xpath('//*[@id="rightout"]/div[1]/ul/li[1]/a').text
# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")
# time.sleep(2)
driver.get(url)

locator = (By.XPATH, "//*[@id='rightout']/div[1]/ul/li[1]/a[not(contains(string(),'%s'))]"%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
#
page=driver.find_element_by_xpath('//*[@id="index"]').text
total=page.strip().split('/')[1]
print(total)
# print(page)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
data=[]

# url=driver.current_url
# rindex = url.rfind('/')
# main_url = url[:rindex]

uls=soup.find('div',class_='menu-list')
lis=uls.find_all('li')
for li in lis:
    # print(li)
    href=li.a['href'].strip('.')
    name=li.a.get_text().strip()
    ggstart_time=li.span.get_text().strip()
    if 'http' in href:
        href=href
    else:
        href='http://www.jdz.gov.cn/'+href

    tmp = [name, ggstart_time,href]
    print(tmp)

# html=driver.page_source
# soup=BeautifulSoup(html,'lxml')
# table=soup.find('table',id='MoreInfoList1_DataGrid1')
# trs=table.find_all('tr')
# for tr in trs:
#     tds=tr.find_all('td')
#     href=tds[1].a['href']
#     href='http://www.gasggzy.com'+href
#     title=tds[1].a['title']
#     date_time=tds[2].get_text().strip()
#     tmp=[title,date_time,href]
#     print(href,title,date_time)


driver.quit()