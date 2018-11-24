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

driver=webdriver.Chrome()
driver.get('http://www.gzzbtbzx.com/more.asp?id=12&city=1&page=2')

locator=(By.XPATH,'//td[@bgcolor="#DFDFDF"]/table[3]/tbody/tr/td/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# time.sleep(1)

val=driver.find_element_by_xpath('//td[@bgcolor="#DFDFDF"]/table[3]/tbody/tr/td/a').text
print(val)
driver.get('http://www.gzzbtbzx.com/more.asp?id=12&city=1&page=1')

locator = (By.XPATH, '//td[@bgcolor="#DFDFDF"]/table[3]/tbody/tr/td/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

main_url=driver.current_url
print(main_url)
main_url=main_url.rsplit('/',maxsplit=1)[0]
print(main_url)
html=driver.page_source
soup=BeautifulSoup(html,'lxml')
content=soup.find('td',attrs={'bgcolor':'#DFDFDF'})
tables=content.find_all('table')
for i in range(2,len(tables)-1):
    table=tables[i]
    tr=table.find('tr')
    tds=tr.find_all('td')
    href=tds[0].a['href']
    if 'http' in href:
        href=href
    else:
        href=main_url+'/'+href
    name=tds[0].a.get_text()
    ggstart_time=tds[1].get_text()
    click_num=tds[2].get_text()

    tmp=[href,name,ggstart_time,click_num]
#
    print(tmp)


driver.quit()


