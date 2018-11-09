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
driver.get('http://www.japrtc.gov.cn/jyxx/jsgc/zbgg/index.htm')

locator=(By.XPATH,"//div[@class='pagingList']/ul/li/a")
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# time.sleep(1)

val=driver.find_element_by_xpath("//div[@class='pagingList']/ul/li/a").text
print(val)
# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")
# time.sleep(2)
driver.get('http://www.japrtc.gov.cn/jyxx/jsgc/zbgg/index.htm')


locator = (By.XPATH, "//div[@class='pagingList']/ul/li/a[not(contains(string(),'%s'))]"%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

page=driver.find_element_by_xpath('//*[@id="div_page"]/a[last()]').get_attribute('href')
total=re.findall(r'index_(\d+).htm',page)[0]
print(total)
print(page)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
trs = soup.find('div', class_='pagingList')
data=[]
url=driver.current_url
rindex = url.rfind('/')
main_url = url[:rindex]
urs=trs.find_all('li')
for tr in urs:
    href = tr.a['href'].strip('.')
    href=main_url+href
    title=tr.a.get_text()
    date_time=tr.span.get_text()
    tmp = [title, href,date_time]
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