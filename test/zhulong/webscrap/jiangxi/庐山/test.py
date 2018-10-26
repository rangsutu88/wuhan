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
driver.get('http://www.lssggzy.gov.cn/xz/xz_type/detailClass/4-45-1')

locator=(By.XPATH,'//*[@id="main"]/div[1]/ul/li[1]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# time.sleep(1)
url=driver.current_url

print(url)
url=url.rsplit('-',maxsplit=1)[0]+'-'+str(2)
print(url)
val=driver.find_element_by_xpath('//*[@id="main"]/div[1]/ul/li[1]/a').text
# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")
# time.sleep(2)
driver.get(url)

locator = (By.XPATH, "//*[@id='main']/div[1]/ul/li[1]/a[not(contains(string(),'%s'))]"%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
#
# page=driver.find_element_by_xpath('//a[@class="clz1"][last()]').get_attribute('href')
# total=re.findall(r'index_(\d+).htm',page)[0]
# print(total)
# print(page)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
uls = soup.find('ul', class_='list')
data=[]
url=driver.current_url
rindex = url.rfind('/')
main_url = url[:rindex]
lis=uls.find_all('li')

for li in lis:
    href = li.a['href']
    href='http://www.lssggzy.gov.cn'+href
    name=li.a.get_text().strip()
    ggstart_time=li.span.get_text()

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