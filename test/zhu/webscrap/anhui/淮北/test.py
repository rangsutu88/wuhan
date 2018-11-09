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
driver.get('http://www.hbzbcg.cn/hbweb/jyxx/002001/002001001/002001001002/MoreInfo.aspx?CategoryNum=002001001002')

#第一个等待
locator=(By.XPATH,'//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url




cnum=driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text
print(cnum)
#第二个等待
val=driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
print(val)

#翻页
num=37
driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))

#翻页

#第二个等待
locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
total=driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text

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
    if '</font>' in name:
        if name.startswith('<font'):
            name=re.findall(r'</font>(.+)',name)[0]
        else:
            name=re.findall(r'(.+)<font',name)[0]
    ggstart_time=tds[2].get_text().strip()

    if 'http' in href:
        href=href
    else:
        href='http://www.hbzbcg.cn'+href

    tmp = [ name, ggstart_time, href]
    print(tmp)

driver.quit()

