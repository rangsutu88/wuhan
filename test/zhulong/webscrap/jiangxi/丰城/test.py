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
driver.get('http://www.fcgzj.gov.cn/Article/ShowClass.asp?ClassID=19&page=1')

locator=(By.XPATH,"//td[@class='main_tdbg_575']/table/tbody/tr/td[2]/a[2]")
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))



html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
tables = soup.find('td', class_='main_tdbg_575')
tds = tables.find_all('a', attrs={'title': not None})
data=[]
for td in tds:

    href = td['href']
    href = 'http://www.fcgzj.gov.cn' + href
    content = td['title']
    name = re.findall('文章标题：(.+)', content)[0]
    ggstart_time = re.findall('更新时间：(\d+-\d+-\d)', content)[0]


    tmp = [name, ggstart_time, href]
    print(tmp)



driver.quit()
