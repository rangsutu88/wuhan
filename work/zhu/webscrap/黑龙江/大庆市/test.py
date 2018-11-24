import re
import time

# from selenium import webdriver
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 初始化
driver = webdriver.Chrome()
driver.get('http://zfcgzx.daqing.gov.cn/jyxxJsgcZbgg/index.htm')


cookies=driver.get_cookies()
cookies=cookies[0]
print(cookies)


# driver.get('http://www.hljcg.gov.cn/xwzs!queryXwxxqx.action?lbbh=42301')

# 第一个等待
locator = (By.XPATH, '//ul[@class="notice-list lf-list1"]/form/li[1]/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
url = driver.current_url

# 寻找当前页
cnum=driver.find_element_by_xpath('//div[@class="pagination"]/a[@class="current"]').text
# print(cnum)

print(cnum)
num=2
url=url.rsplit('/',maxsplit=1)[0]+'/index_'+str(num)+'.htm'


print(url)

# 第二个等待
val = driver.find_element_by_xpath('//ul[@class="notice-list lf-list1"]/form/li[1]/a').text
print(val)

# 翻页
#
# driver.execute_script("javascript:jump('2');return false;")

# 翻页
# driver.delete_all_cookies()
driver.add_cookie(cookies)

driver.get(url)

# 第二个等待
locator = (By.XPATH, '//ul[@class="notice-list lf-list1"]/form/li[1]/a[not(contains(string(),"%s"))]' % val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

# 获取总页数
page = driver.find_element_by_xpath('//div[@class="pagination"]/a[last()]').get_attribute('href')

page=re.findall('index_(\d+).htm',page)[0]
total = int(page)
print(total)

data = []

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div = soup.find('div', class_='infor-con2 on')
divs = div.find_all('li')

for li in divs:
    href = li.a['href']
    name = li.a.get_text()
    ggstart_time=li.span.get_text()
    if 'http' in href:
        href = href
    else:
        href = 'http://zfcgzx.daqing.gov.cn'+href
    tmp = [name, ggstart_time,href]
    print(tmp)

driver.quit()




