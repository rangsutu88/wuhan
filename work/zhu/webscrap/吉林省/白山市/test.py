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
driver.get('http://www.bsggzyjy.gov.cn/jyxx/003001/003001001/1.html')
# except:
    # driver.execute_script('javascript:window.stop()')

#第一个等待
locator=(By.XPATH,'//ul[@class="wb-data-item"]/li[1]/div/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url
cnum=re.findall('/(\d+?).html',url)[0]


num=2
url=url.rsplit('/',maxsplit=1)[0]+'/'+str(num)+'.html'


print(cnum)


#第二个等待
val=driver.find_element_by_xpath('//ul[@class="wb-data-item"]/li[1]/div/a').text
print(val)

#翻页


driver.get(url)
# 第二个等待
locator = (By.XPATH, '//ul[@class="wb-data-item"]/li[1]/div/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


page=driver.find_element_by_xpath('//li[@class="ewb-page-li ewb-page-noborder ewb-page-num"]/a').get_attribute('href')
print(page)
total=re.findall('/(\d+?).html',page)[0]
print(total)


#获取总页数


data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('ul',class_='wb-data-item')
trs=div.find_all('li')
print(len(trs))

for tr in trs:

    href=tr.div.a['href']
    name=tr.div.a.get_text()
    ggstart_time=tr.span.get_text()

    if 'http' in href:
        href=href
    else:
        href='http://www.bsggzyjy.gov.cn'+href

    tmp = [name, ggstart_time, href]

    print(tmp)


driver.quit()

