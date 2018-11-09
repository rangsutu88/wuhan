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
driver.get('http://www.gasggzy.com/gasggzy/gcjs/009001/009001001/MoreInfo.aspx?CategoryNum=009001001')

# time.sleep(1)
# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")
# time.sleep(2)
locator=(By.XPATH,'//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
page_all=driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text
print(page_all)
# time.sleep(4)

html=driver.page_source
soup=BeautifulSoup(html,'lxml')
table=soup.find('table',id='MoreInfoList1_DataGrid1')
trs=table.find_all('tr')
for tr in trs:
    tds=tr.find_all('td')
    href=tds[1].a['href']
    href='http://www.gasggzy.com'+href
    title=tds[1].a['title']
    date_time=tds[2].get_text().strip()
    tmp=[title,date_time,href]
    print(href,title,date_time)


driver.quit()