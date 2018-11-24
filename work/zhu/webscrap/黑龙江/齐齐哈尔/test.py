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
driver.get('http://www.qqhrggzy.cn/jyxx/003001/003001001/about.html')





# driver.get('http://www.hljcg.gov.cn/xwzs!queryXwxxqx.action?lbbh=42301')

# 第一个等待
locator = (By.XPATH, '//ul[@class="wb-data-item"]/li[1]/div/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
url = driver.current_url

# 寻找当前页
cnum=driver.find_element_by_xpath('//span[@id="index"]').text.strip()
# print(cnum)
cnum = re.findall('(\d+)/', cnum)[0]
print(cnum)
num=2
url=url.rsplit('/',maxsplit=1)[0]+'/'+str(num)+'.html'


print(url)

# 第二个等待
val = driver.find_element_by_xpath('//ul[@class="wb-data-item"]/li[1]/div/a').text
print(val)

# 翻页
#
# driver.execute_script("javascript:jump('2');return false;")

# 翻页

driver.get(url)

# 第二个等待
locator = (By.XPATH, '//ul[@class="wb-data-item"]/li[1]/div/a[not(contains(string(),"%s"))]' % val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

# 获取总页数
page = driver.find_element_by_xpath('//span[@id="index"]').text

page=re.findall('/(\d+)',page)[0]
total = int(page)
print(total)

data = []

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div = soup.find('ul', class_='wb-data-item')
divs = div.find_all('li',class_="wb-data-list")

for li in divs:
    href = li.div.a['href']
    name = li.div.a.get_text()
    ggstart_time=li.span.get_text()
    if 'http' in href:
        href = href
    else:
        href = 'http://www.qqhrggzy.cn'+href

    tmp = [name, ggstart_time,href]
    print(tmp)

driver.quit()




