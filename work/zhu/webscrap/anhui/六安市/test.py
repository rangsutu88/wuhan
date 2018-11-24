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
driver.get('http://www.laztb.gov.cn/laztb/jyxx/002001/002001001/002001001003/')

#第一个等待
locator=(By.XPATH,'//font[@class="currentpostionfont01"]/../font[2]/a[4]')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

c_type=driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[4]').text.strip()

url=driver.current_url
try:
    driver.switch_to.frame(1)
    mark=1
except:
    mark=0



cnum=driver.find_element_by_xpath('//td[@class="huifont"]').text
cnum=re.findall('(\d+)/',cnum)[0]
print(cnum)
#第二个等待
val=driver.find_element_by_xpath('//li[@class="ewb-plate-list clearfix"]/a').text
print(val)
num=2

# driver.get(url)
#翻页

if c_type=='招标公告':
    mark_1 = url.strip('/').rsplit('/', maxsplit=1)[1]
    driver.execute_script("window.location.href='./morezbgg.aspx?CategoryNum={}&Paging={}'".format(mark_1,num))
else:
    driver.execute_script("window.location.href='./?Paging={}'".format(num))


url=driver.current_url
print(url)

#第二个等待

locator = (By.XPATH, '//li[@class="ewb-plate-list clearfix"]/a[not(contains(string(),"{}"))]'.format(val))
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
total=driver.find_element_by_xpath('//td[@class="huifont"]').text
total=re.findall('\/(\d+)',total)[0]

total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
trs=soup.find_all('li',class_="ewb-plate-list clearfix")

for tr in trs:
    href=tr.a['href']
    name=tr.a['title']

    ggstart_time=tr.span.get_text()
    if 'http' in href:
        href=href
    else:
        href='http://www.laztb.gov.cn'+href

    tmp = [ name, ggstart_time, href]
    print(tmp)

driver.quit()

