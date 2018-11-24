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
driver.get('http://www.hgggzyjyw.org.cn/gcjs/014001/1.html')



# driver.get('http://www.hljcg.gov.cn/xwzs!queryXwxxqx.action?lbbh=42301')

# 第一个等待
locator = (By.XPATH, '//ul[@class="ewb-info-items"]/li[1]/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
url = driver.current_url

# 寻找当前页
cnum=driver.find_element_by_xpath('//span[@id="index"]').text
# print(cnum)
cnum=re.findall('(\d+)/',cnum)[0]
print(cnum)
num=2
url=url.rsplit('/',maxsplit=1)[0]+'/'+str(num)+'.html'


print(url)

# 第二个等待
val = driver.find_element_by_xpath('//ul[@class="ewb-info-items"]/li[1]/a').text
print(val)

# 翻页
#
# driver.execute_script("javascript:jump('2');return false;")

# 翻页


# 第二个等待
locator = (By.XPATH, '//ul[@class="ewb-info-items"]/li[1]/a[not(contains(string(),"%s"))]' % val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

# 获取总页数
page = driver.find_element_by_xpath('//span[@id="index"]').text

page=re.findall('/(\d+)',page)[0]
total = int(page)
print(total)

data = []

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div = soup.find('ul', class_='ewb-info-items')
divs = div.find_all('li')

for li in divs:
    href = li.a['href']
    name = li.a['title']
    ggstart_time=li.span.get_text().strip()
    if 'http' in href:
        href = href
    else:
        href = 'http://www.hgggzyjyw.org.cn'+href
    tmp = [name, ggstart_time,href]
    print(tmp)

driver.quit()




