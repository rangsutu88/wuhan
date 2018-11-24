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
driver.get('http://www.hljcg.gov.cn/xwzs!queryXwxxqx.action?lbbh=42301')

# 第一个等待
locator = (By.XPATH, '//div[@class="yahoo"]/div[1]/span/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
url = driver.current_url

# 寻找当前页
cnum=driver.find_element_by_xpath('//div[@class="yahoo2"]/div/span/b[2]').text.strip()
# print(cnum)
cnum = re.findall('(\d+)/', cnum)[0]
print(cnum)
num=1

print(url)

# 第二个等待
val = driver.find_element_by_xpath('//div[@class="yahoo"]/div[1]/span/a').text
print(val)

# 翻页

driver.execute_script("javascript:jump('2');return false;")

# 翻页

# driver.get(url)

# 第二个等待
locator = (By.XPATH, '//div[@class="yahoo"]/div[1]/span/a[not(contains(string(),"%s"))]' % val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

# 获取总页数
page = driver.find_element_by_xpath('//div[@class="yahoo2"]/div/span/b[2]').text

page=re.findall('/(\d+)',page)[0]
total = int(page)
print(total)

data = []

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div = soup.find('div', class_='yahoo')
divs = div.find_all('div',class_="xxei")

for li in divs:
    href = li.find('span',class_="lbej").a['onclick']
    name = li.find('span',class_="lbej").a.get_text()
    ggstart_time = li.find('span',class_="sjej").get_text()
    address = li.find('span',class_="nrej").get_text()
    href=re.findall('javascript:location.href=(.+);return false',href)[0].strip("'")

    if 'http' in href:
        href = href
    else:
        href = 'http://www.hljcg.gov.cn'+href

    tmp = [name, ggstart_time,href,address]
    print(tmp)

driver.quit()




