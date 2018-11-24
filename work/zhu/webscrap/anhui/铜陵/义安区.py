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

driver.get('http://yaq.tlzbcg.com/yaqztb/jyxx/008001/008001001/?Paging=1')

#第一个等待
# locator=(By.XPATH,'//ul[@class="mored"]/li[1]/div/a')
locator = (By.XPATH, '//*[@id="DataGrid1"]/tbody/tr[1]/td[2]/a | //table[@class="moreinfocon"]/tbody/tr[1]/td[2]/a | //ul[@class="mored"]/li[1]/div/a')
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
val=driver.find_element_by_xpath('//ul[@class="mored"]/li[1]/div/a').text
print(val)

#翻页

# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")

#翻页
num=2
url=main_url+'='+str(num)
print(url)
driver.get(url)

#第二个等待
locator = (By.XPATH, '//ul[@class="mored"]/li[1]/div/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
page=driver.find_element_by_xpath('//div[@class="pageText xxxsHidden"][1] | //td[@class="huifont"]').text
print(page)
total=re.findall('/(\d+)',page)[0]
total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('ul',class_='mored')
trs=div.find_all('li')

for li in trs:
    ggstart_time=li.i.get_text()
    ggstart_time=re.findall('\[(.+\])',ggstart_time)[0]
    href=li.div.a['href']
    name=li.div.a['title']

    if 'http' in href:
        href=href
    else:
        if 'zyx' in url:
            href = 'http://zyx.tlzbcg.com' + href
        elif 'yaq' in url:
            href = 'http://yaq.tlzbcg.com' + href
        else:
            href = href

    tmp = [name, ggstart_time, href]

    print(tmp)

driver.quit()

