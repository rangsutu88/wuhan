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
driver.get('http://www.srjsgc.cn/news/list.php?catid=4&page=1')

locator=(By.XPATH,"/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[1]/a")
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# time.sleep(1)
cnum=driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[42]/td/div/strong').text.strip()
print(cnum)
url=driver.current_url
main_url=url.rsplit('=')[0]
print(main_url)
val=driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[1]/a").text
print(val)
# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")
# time.sleep(2)
driver.get('http://www.srjsgc.cn/news/list.php?catid=4&page=2')


locator = (By.XPATH, "/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[1]/a[not(contains(string(),'%s'))]"%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

page=driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[42]/td/div/cite').text
total=re.findall('条/(\d+)页',page)[0]
print(total)




html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
trs=soup.find_all('tr',height=27)
for tr in trs:
    tds=tr.find_all('td')
    href=tds[0].a['href']
    name=tds[0].a.get_text()
    ggstart_time=tds[1].get_text()
    if 'http' in href:
        href=href
    else:
        href=None

    tmp = [name, href,ggstart_time]
    print(tmp)



driver.quit()