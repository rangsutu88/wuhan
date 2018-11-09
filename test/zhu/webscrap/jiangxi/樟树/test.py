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
driver.get('http://www.zsggzy.com/news_,11,12,22,_%D5%FE%B8%AE%B2%C9%B9%BA_1___.html')

locator=(By.XPATH,'/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# time.sleep(1)

# val=driver.find_element_by_xpath('//*[@id="infolist"]/li[1]/div/a').text
# print(val)
# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")
# time.sleep(2)
num=2
# driver.get('http://www.gaztbw.gov.cn/jyxx/001001/.html')
url=driver.current_url
page=re.findall('_(\d+)___.html',url)[0]
if int(page)!=num:
    s = "_%d___.html"%num
    url = re.sub("_[0-9]+___.html", s, url)
    print(url)

    val=driver.find_element_by_xpath("//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a").text
    print(val)
    driver.get(url)

    locator = (By.XPATH, "//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a[string()!='%s']" % val)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    text=driver.find_element_by_xpath('/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td/text()[6]')
    print(text)


page=driver.find_element_by_xpath("//table[@class='bg04']/tbody/tr[2]/td/table/tbody/tr[2]/td/a[last()]").get_attribute('href')
total=re.findall('_(\d+)___.html',page)[0]
# print(total)
#
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
tables=soup.find('table',attrs={'width':650})
trs=tables.find_all('tr')
for i in range(0,len(trs),2):
    tr=trs[i]
    href=tr.td.a['href']
    href='http://www.zsggzy.com/'+href
    name=tr.td.a.get_text()
    ggstart_time=tr.find('td',class_='newsdate').get_text().strip(']').strip('[')
    print(ggstart_time)
    print(name)
    print(href)
    # print(tr)
# print(table[0])
# print(table[1])
# trs=table.find_all('tr')
# for tr in trs:
#     print(tr)
# print(table)
# trs=soup.find_all('tr')
# print(len(trs))

driver.quit()