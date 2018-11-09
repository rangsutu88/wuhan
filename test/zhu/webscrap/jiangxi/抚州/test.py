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
driver.get('http://www.fzztb.gov.cn/jsgc/zbgg/index.htm')


locator=(By.XPATH,"//table[@class='bg'][1]/tbody/tr/td/a")
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

page=driver.find_element_by_xpath("(//*[@class='cy05'])[last()]").get_attribute('href')
total=re.findall(r'index_(\d+).htm',page)[0]
print(total)
print(page)


html=driver.page_source
soup=BeautifulSoup(html,'lxml')

tables=soup.find_all('table',class_='bg')
for table in tables:
    tds=table.find_all('td')
    name=tds[0].a['title']
    href=tds[0].a['href']
    ggstart_time=tds[1].get_text()


    tmp=[name,ggstart_time,href]
    print(tmp)
    # data.append(tmp)


driver.quit()