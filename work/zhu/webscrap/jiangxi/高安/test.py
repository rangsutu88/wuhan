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
driver.get('http://www.gaztbw.gov.cn/jyxx/001001/001001001/secondpageJyMk.html')

locator=(By.XPATH,'//*[@id="infolist"]/li[1]/div/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# time.sleep(1)

# val=driver.find_element_by_xpath('//*[@id="infolist"]/li[1]/div/a').text
# print(val)
# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")
# time.sleep(2)
num=2
# driver.get('http://www.gaztbw.gov.cn/jyxx/001001/.html')
url=driver.current_url
if "secondpageJyMk.html" in url:
    cnum=1
else:
    cnum=int(re.findall("([0-9]{1,}).html",url)[0])
    print(cnum)
if num!=cnum:
    print('here')
    if num==1:
        url=re.sub("[0-9]{1,}.html","secondpageJyMk.html",url)
    else:
        s="/%d.html"%(num)
        print(s)
        url=url.rsplit('/',maxsplit=1)[0]+s

    print(url)
    val=driver.find_element_by_xpath('//*[@id="infolist"]/li[1]/div/a').text
    print(val)
    driver.get(url)
    print(url)

    locator = (By.XPATH, "//*[@id='infolist']/li[1]/div/a[string()!='%s']" % val)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


page=driver.find_element_by_xpath('//*[@id="page"]/ul/li[10]/a').text


print(page)
#
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
trs = soup.find('ul', class_='wb-data-item')
data=[]
url=driver.current_url

urs=trs.find_all('li')
for tr in urs:
    href = tr.a['href'].strip('.')
    href='http://www.gaztbw.gov.cn'+href
    title=tr.a.get_text()
    date_time=tr.span.get_text()
    tmp = [title, href,date_time]
    print(tmp)
#


driver.quit()