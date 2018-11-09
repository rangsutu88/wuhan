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
driver.maximize_window()
driver.get('http://www.aqzbcg.org:1102/jyxx/012001/012001001/2.html')

#第一个等待
locator=(By.XPATH,'//ul[@class="wb-data-item"]/li/div/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url
main_url=url.rsplit('/',maxsplit=1)[0]
print(main_url)

#寻找当前页


cnum=re.findall(r'/(\d+)\.html',url)[0]
print(cnum)


#第二个等待
val=driver.find_element_by_xpath('//ul[@class="wb-data-item"]/li[1]/div/a').text
print(val)

#翻页

# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")

#翻页
num=3
url=main_url+'/'+str(num)+'.html'
driver.get(url)


#第二个等待
locator = (By.XPATH, '//*[@id="jt"]/ul/li[1]/div/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


#获取总页数
page=driver.find_element_by_xpath('//li[@class="wb-page-li"][1]/span').text
print(page)
total=re.findall('/(\d+)',page)[0]
total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('ul',class_='wb-data-item')
lis=div.find_all('li')

for tr in lis:

    div=tr.find('div')
    href=div.a['href']
    content=div.a['title']
    ggstart_time=tr.find('span',recursive=False).get_text()
    if 'http' in href:
        href=href
    else:
        href='http://www.aqzbcg.org:1102'+href
    tmp = [content, ggstart_time, href]
    print(tmp)

driver.quit()

