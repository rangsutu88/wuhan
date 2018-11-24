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
driver.get('http://www.dxs.gov.cn/news-list-zfcg-1.html')

#第一个等待
locator=(By.XPATH,'//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url


#寻找当前页
# cnum=driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span').text.strip()
# print(cnum)
cnum=re.findall('-(\d+?)\.html',url)[0]
print(cnum)
main_url=url.rsplit('-',maxsplit=1)[0]
print(main_url)

#第二个等待
val=driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span').text
print(val)

#翻页

# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")

#翻页

driver.get('http://www.dxs.gov.cn/news-list-zfcg-2.html')

#第二个等待
locator = (By.XPATH, '//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
page=driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[3]/div[2]/a[4]').get_attribute('href')

total=re.findall('-(\d+?)\.html',page)[0]
total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('div',class_='lb_ul')
lis=div.find_all('li')
for li in lis:
    href=li.a['href']
    name=li.a.span.get_text()
    ggstart_time=li.find('span',class_='sp2').get_text()


    if 'http' in href:
        href=href
    else:
        href=None

    tmp = [name, href,ggstart_time]
    print(tmp)

driver.quit()