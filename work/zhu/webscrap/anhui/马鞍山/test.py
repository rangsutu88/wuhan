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
driver.get('http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001002/028001002001/MoreInfo.aspx?CategoryNum=028001002001')

#第一个等待
locator=(By.XPATH,'//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url


#寻找当前页
# cnum=driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span').text.strip()
# print(cnum)

# cnum=driver.find_element_by_xpath('//*[@id="Pager"]/table/tbody/tr/td[1]/font[3]/b').text
# print(cnum)
#第二个等待
val=driver.find_element_by_xpath('//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a').text
print(val)

#翻页
num=1
driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))

#翻页

#第二个等待
locator = (By.XPATH, '//td[@id="MoreInfoList1_tdcontent"]/table/tbody/tr[1]/td[2]/a')
WebDriverWait(driver, 10).until_not(EC.text_to_be_present_in_element(locator,val))

#获取总页数
total=driver.find_element_by_xpath('//div[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text

total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('table',id='MoreInfoList1_DataGrid1')
trs=div.find_all('tr',valign='top')
print(len(trs))

for tr in trs:
    tds=tr.find_all('td')
    href=tds[1].a['href']
    name=tds[1].a['title']
    ggstart_time=tds[2].get_text().strip()

    if 'http' in href:
        href=href
    else:
        href='http://zbcg.mas.gov.cn'+href

    tmp = [ name, ggstart_time, href]
    print(tmp)

driver.quit()

