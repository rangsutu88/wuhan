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

# driver.set_page_load_timeout(3)
# try:
driver.get('http://ggzy.liaoyuan.gov.cn/xxgk/zhaobgg/index.html')
# except:
    # driver.execute_script('javascript:window.stop()')

#第一个等待
locator=(By.XPATH,'//ul[@class="ly_list"]/li[1]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url
if 'index.html' in url:
    cnum=1
else:
    cnum=re.findall('index_(\d+).html',url)[0]
    cnum=int(cnum)+1

num=2
url=url.rsplit('/',maxsplit=1)[0]+'/index_'+str(num)+'.html'


print(cnum)


#第二个等待
val=driver.find_element_by_xpath('//ul[@class="ly_list"]/li[1]/a').text
print(val)

#翻页

driver.get(url)
# 第二个等待
locator = (By.XPATH, '//ul[@class="ly_list"]/li[1]/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


page=driver.find_element_by_xpath('//div[@class="ly_ggzyjyzx_page_tzgg"]/div[2]/a[last()]').get_attribute('href')
total=re.findall('index_(\d+).html',page)
print(total)

#获取总页数


data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('ul',class_='ly_list')
trs=div.find_all('li',attrs={'class':''})
print(len(trs))
url=driver.current_url
main_url=url.rsplit('/',maxsplit=1)[0]
for tr in trs:


    href=tr.a['href'].strip('.')
    name=tr.a.get_text()
    ggstart_time=tr.span.get_text()

    if 'http' in href:
        href=href
    else:
        href=main_url+href

    tmp = [name, ggstart_time, href]

    print(tmp)


driver.quit()

