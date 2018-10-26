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
driver.get('http://jgszb.jgs.gov.cn/html/jsgcgg/index.html')

locator=(By.XPATH,"//div[@class='list2']/span/ul/li[1]/a")
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

# time.sleep(1)

val=driver.find_element_by_xpath("//div[@class='list2']/span/ul/li[1]/a").text
driver.execute_script("goClass_nextPage();")
# time.sleep(2)

locator = (By.XPATH, "//div[@class='list2']/span/ul/li[1]/a[not(contains(string(),'%s'))]"%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

# print(driver.find_element_by_xpath("//div[@class='list2']/span").text)

page_all=driver.find_element_by_xpath("//div[@class='list2']/span").text
total=re.findall('/(\d+)页',page_all)[0]
page = re.findall('页次：(\d+)/', page_all)[0]
print(total)
print(page)
# time.sleep(4)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
tables=soup.find('div',class_='list2')
span=tables.find('span')
lis=span.find_all('li')
for li in lis:
    href=li.a['href']
    if 'http' in href:
        href=href
    else:
        href='http://jgszb.jgs.gov.cn'+href
    ggstart_time=li.span.get_text()
    name=li.a.get_text()
    tmp=[name,ggstart_time,href]
    print(tmp)




driver.quit()