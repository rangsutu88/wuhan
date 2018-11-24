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
driver.get('http://whsggzy.wuhu.gov.cn/jyxx/005001/005001004/17.html')

#第一个等待
locator=(By.XPATH,'//table[@class="ewb-table"]/tbody/tr[1]/td[2]/a')
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
val=driver.find_element_by_xpath('//table[@class="ewb-table"]/tbody/tr[1]/td[2]/a').text
print(val)

#翻页

# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")

#翻页
num=18
url=main_url+'/'+str(num)+'.html'
print(url)
driver.get(url)

#第二个等待
locator = (By.XPATH, '//table[@class="ewb-table"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
page=driver.find_element_by_xpath('//div[@class="ewb-page"]/ul/li[last()-3]/span').text
print(page)
total=re.findall('/(\d+)',page)[0]
total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('table',class_='ewb-table')
tbody=div.find('tbody')
trs=tbody.find_all('tr')
for tr in trs:

    tds=tr.find_all('td')
    address=tds[1].span.get_text().strip(']').strip('[')
    href=tds[1].a['href']
    content=tds[1].a['title']
    if '</font>' in content:
        status=re.findall('\[(.+)\]',content)[0]
        name=re.findall(r'</font>(.+)',content)[0]
    else:
        status=None
        name=content
    ggstart_time=tds[2].get_text()


    if 'http' in href:
        href=href
    else:
        href='http://whsggzy.wuhu.gov.cn'+href

    tmp = [address,status, name, ggstart_time, href]

    print(tmp)

driver.quit()

