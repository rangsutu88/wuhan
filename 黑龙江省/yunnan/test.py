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
driver.get('http://www.tcsggzyjyw.com/Jyweb/PBJGGSList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=1&SubType2=24')

#第一个等待
locator=(By.XPATH,'//div[@class="boxcontent"]/table/tbody/tr[2]/td[3]')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url



#寻找当前页

cnum=driver.find_element_by_xpath('//span[@id="lblAjax_PageIndex"]').text.strip()
print(cnum)
# cnum=re.findall('-(\d+?)\.html',url)[0]
# print(cnum)
# main_url=url.rsplit('-',maxsplit=1)[0]
# print(main_url)

#第二个等待
val=driver.find_element_by_xpath('//div[@class="boxcontent"]/table/tbody/tr[2]/td[3]').text
print(val)
num=2
#翻页

input_page=driver.find_element_by_xpath('//div[@class="pager"]/table/tbody/tr/td[1]/input')
input_page.clear()
input_page.send_keys(num,Keys.ENTER)

#翻页

# driver.get('http://www.dxs.gov.cn/news-list-zfcg-2.html')

#第二个等待
locator = (By.XPATH, '//div[@class="boxcontent"]/table/tbody/tr[2]/td[3][not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
page=driver.find_element_by_xpath('//span[@id="lblAjax_TotalPageCount"]').text

total=int(page)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('div',class_='boxcontent').find('table')
trs=div.find_all('tr')
for i in range(1,len(trs)):
    tr=trs[i]
    tds=tr.find_all('td')
    href=tds[2].a['href']
    name=tds[2].a.get_text()
    index_num=tds[1].get_text()
    ggstart_time=tds[3].get_text()

    if 'http' in href:
        href=href
    else:
        href='http://www.tcsggzyjyw.com/Jyweb/'+href

    tmp = [index_num,name, href,ggstart_time]
    print(tmp)

driver.quit()

