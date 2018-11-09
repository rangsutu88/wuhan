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
driver.get('http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001003/003001003002/')

#第一个等待
locator=(By.XPATH,'//*[@id="MoreInfoList1_moreinfo"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

'(//font[@color="red"])[1]/../../../following-sibling::tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/a'

'//*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a'

cnum=driver.find_element_by_xpath('//td[@class="huifont"]').text
cnum=re.findall('(\d+)/',cnum)[0]
print(cnum)
#第二个等待
val=driver.find_element_by_xpath('//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a').text
print(val)
num=2

# driver.get(url)
#翻页

try:
    driver.execute_script("ShowNewPage('moreinfo.aspx?Paging={}');".format(num))
except:
    driver.execute_script("window.location.href='./moreinfo.aspx?Paging={}'".format(num))


#第二个等待

locator = (By.XPATH, '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a[not(contains(string(),"{}"))]'.format(val))
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
total=driver.find_element_by_xpath('//td[@class="huifont"]').text
total=re.findall('\/(\d+)',total)[0]

total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('td',align="right")
tbody=div.find('tbody')
trs=tbody.find_all('tr',height='30px',recursive=False)

for tr in trs:
    table=tr.find('table')
    tds=table.find_all('td')

    href=tds[-2].a['href']
    name=tds[-2].a['title']
    ggstart_time=tds[-1].get_text()

    if 'http' in href:
        href=href
    else:
        href='http://www.bzztb.gov.cn'+href

    tmp = [ name, ggstart_time, href]
    print(tmp)

driver.quit()

