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
driver.get('http://www.yingtan.gov.cn/xxgk/zdgc/zdgcztb/index_2.htm')


locator=(By.XPATH,"//div[@class='ldjs_body']/ul/li/a")
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

page=driver.find_element_by_xpath("(//*[@class='cn'])[5]").text
total=re.findall('总共(\d+)页',page)[0]
print(total)

page=driver.page_source

soup=BeautifulSoup(page,"lxml")
url=driver.current_url
rindex=url.rfind('/')
url_1=url[:rindex]
url_2=re.findall('http://www.yingtan.gov.cn/\w+?/',url)[0]
print(url_2)
tables=soup.find('div',class_='ldjs_body')
lis=tables.find_all('li')
data=[]
for i in range(0,len(lis),2):
    # print(li)
    li=lis[i]
    href=li.a['href'].strip('.')
    print(href)
    title=li.get_text().strip().strip('•').strip()
    li=lis[i+1]
    data_time=li.get_text().strip()
    if re.findall('http',href):
        href=href
    elif re.findall(r'/\.\./',href):
        href=href.split(r'/../')[1]
        href=url_2+href
    else:
        href=url_1+href

    tmp=[title,data_time,href]
    print(tmp)
    data.append(tmp)


driver.quit()