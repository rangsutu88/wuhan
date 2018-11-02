import re
import time
import pandas as pd
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
driver.get('http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=20&cut=&page=1')

locator = (By.XPATH, "//td[@bgcolor='#DFDFDF']/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a")
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

url='http://gcjs.gzzbtbzx.com:88/zbgg/more_ze.asp?keyword=&dq=20&cut=&page={}'.format(2)
val = driver.find_element_by_xpath("//td[@bgcolor='#DFDFDF']/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a").text
driver.get(url)
try:
    locator = (By.XPATH,
     '//td[@bgcolor="#DFDFDF"]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/a[not(contains(string(),"%s"))]' % val)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
except:
    time.sleep(1)

main_url = driver.current_url


data = []
main_url = main_url.rsplit('/', maxsplit=1)[0]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
content = soup.find('td', attrs={'bgcolor': '#DFDFDF'})
table = content.find_all('table')
table = table[1]
trss = table.find('table').find('table')
trs = trss.find_all('tr')

for i in range(3, len(trs), 2):
    tr = trs[i]
    tds = tr.find_all('td')
    href = tds[0].a['href']
    if 'http' in href:
        href = href
    else:
        href = main_url + '/' + href
    name = tds[0].a.get_text()
    ggstart_time = tds[2].get_text()
    click_num = tds[4].get_text()
    tmp = [ name, ggstart_time, click_num,href]
    print(tmp)





driver.quit()