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
driver.get('http://www.jjjsj.gov.cn/csjs/jzgc/index.html')

locator=(By.XPATH,'//*[@id="comp_5790085"]/div/ul[1]/li[1]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# time.sleep(1)

val=driver.find_element_by_xpath('//*[@id="comp_5790085"]/div/ul[1]/li[1]/a').text
# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")
# time.sleep(2)
driver.get('http://www.jjjsj.gov.cn/csjs/jzgc/index_1.html')

locator = (By.XPATH, "//*[@id='comp_5790085']/div/ul[1]/li[1]/a[not(contains(string(),'%s'))]"%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

page=driver.find_element_by_xpath("//font[@class='fystyle'][last()-1]").text
total=re.findall('总共(\d+)页',page)[0]
print(total)

main_url=driver.current_url
main_url=main_url.rsplit('/',maxsplit=1)[0]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('div',class_='clist_con')
lis=div.find_all('li')
for li in lis:
    href=li.a['href'].strip('.')
    if 'http' in href:
        href=href
    else:
        href=main_url+href
    name=li.a.get_text().strip()
    ggstart_time=li.span.a.get_text()
    tmp = [name, href,ggstart_time]
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