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
driver.maximize_window()
driver.get('http://www.lushan.gov.cn/public/column/4443193?type=4&catId=5336732&action=list')

locator=(By.XPATH,"//div[@class='xxgk_navli'][1]/ul/li[3]/a")
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

num=2
val=driver.find_element_by_xpath("//div[@class='xxgk_navli'][1]/ul/li[3]/a").text

cpage=driver.find_element_by_xpath('//*[@id="page_public_info"]/span[4]/input')
cpage.clear()
cpage.send_keys(num,Keys.ENTER)


locator = (By.XPATH, "//div[@class='xxgk_navli'][1]/ul/li[3]/a[not(contains(string(),'%s'))]"%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
#
total=driver.find_element_by_xpath('//*[@id="page_public_info"]/a[last()]').get_attribute('paged')
print(total)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
divs=soup.find_all('div',class_='xxgk_navli')
for div in divs:
    lis=div.find_all('li')
    index=lis[1].get_text()
    href=lis[2].a['href']
    name=lis[2].a.get_text()
    ggstart_time=lis[3].get_text()
    tmp=[index,name,ggstart_time,href]
    print(tmp)





driver.quit()