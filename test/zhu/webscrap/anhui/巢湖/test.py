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
driver.get('http://www.hfggzy.com/chzbtb//showinfo/moreinfolist.aspx?categorynum=003001001&Paging=1')

#第一个等待
locator=(By.XPATH,'//*[@id="form1"]/div[3]/table/tbody/tr[1]/td[2]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url


#寻找当前页
# cnum=driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span').text.strip()
# print(cnum)

cnum=re.findall('Paging=(\d+)',url)[0]
print(cnum)
main_url=url.rsplit('=',maxsplit=1)[0]
print(main_url)

#第二个等待
val=driver.find_element_by_xpath('//*[@id="form1"]/div[3]/table/tbody/tr[1]/td[2]/a').text
print(val)

#翻页

# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")

#翻页
num=2
url=main_url+'='+str(num)
print(url)
driver.get(url)

#第二个等待
locator = (By.XPATH, '//*[@id="form1"]/div[3]/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
page=driver.find_element_by_xpath('//td[@class="huifont"]').text
print(page)
total=re.findall('/(\d+)',page)[0]
total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('form',id='form1')
table=div.find('table')
trs=table.find_all('tr')

for tr in trs:

    tds=tr.find_all('td')
    href=tds[1].a['href']
    name=tds[1].a['title']
    try:
        status=tds[1].font.get_text().strip('[').strip(']')
    except Exception as e:
        status=0

    ggstart_time=tds[2].get_text()


    if 'http' in href:
        href=href
    else:
        href='http://www.hfggzy.com'+href

    tmp = [name,status, ggstart_time, href]

    print(tmp)

driver.quit()

