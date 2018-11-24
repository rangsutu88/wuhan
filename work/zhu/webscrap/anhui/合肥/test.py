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
driver.get('http://ggzy.hefei.gov.cn/jyxx/002001/002001001/2000.html')

#第一个等待
locator=(By.XPATH,'/html/body/ul/li[1]/a/span[3]')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url


#寻找当前页
# cnum=driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span').text.strip()
# print(cnum)

cnum=re.findall('\/(\d+?).html',url)[0]
print(cnum)
main_url=url.rsplit('/',maxsplit=1)[0]
print(main_url)

#第二个等待
val=driver.find_element_by_xpath('/html/body/ul/li[1]/a/span[3]').text
print(val)

#翻页

# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")

#翻页
num=1888
url=main_url+'/'+str(num)+'.html'
print(url)
driver.get(url)

#第二个等待
locator = (By.XPATH, '/html/body/ul/li[1]/a/span[3][not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
page=driver.find_element_by_xpath('//*[@id="index"]').text
print(page)
total=re.findall('/(\d+)',page)[0]
total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('ul',class_='ewb-right-item')
lis=div.find_all('li')
for li in lis:
    address=li.find('span',class_='ewb-label1 l').get_text().strip('】').strip('【')
    try:
        status=li.find('span',class_='ewb-label2 l').get_text().strip().strip('】').strip('【')
    except:
        status=li.find('span',class_='ewb-label2 l hidden').get_text().strip('】').strip('【')
    href=li.a['href'].strip('.')
    name=li.find('span',class_='ewb-context l').get_text()
    ggstart_time=li.find('span',recursive=False).get_text()


    if 'http' in href:
        href=href
    else:
        href='http://ggzy.hefei.gov.cn'+href


    if status=='':
        tmp = [address, name, ggstart_time, href]
    else:
        tmp = [address,status,name,ggstart_time,href]
    print(tmp)

driver.quit()

