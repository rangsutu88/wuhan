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
driver.get('http://www.hljggzyjyw.gov.cn/trade/tradezfcg?cid=16&pageNo=1&type=1&notice_name=')

# 第一个等待
locator = (By.XPATH, '//div[@class="news_inf"]/div/ul/li/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
url = driver.current_url

# 寻找当前页
# cnum=driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[2]/ul[1]/li[1]/a/span').text.strip()
# print(cnum)
cnum = re.findall('pageNo=(\d+)&', url)[0]
print(cnum)
num=2
print(url)
url=re.sub('pageNo=(\d+)&','pageNo='+str(num)+'&',url)
print(url)

# 第二个等待
val = driver.find_element_by_xpath('//div[@class="news_inf"]/div/ul/li/a').text
print(val)

# 翻页

# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")

# 翻页

driver.get(url)

# 第二个等待
locator = (By.XPATH, '//div[@class="news_inf"]/div/ul/li/a[not(contains(string(),"%s"))]' % val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

# 获取总页数
page = driver.find_element_by_xpath('//div[@class="page"]/span[2]/b[2]').text

total = int(page)
print(total)

data = []

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div = soup.find('div', class_='right_box')
ul = div.find('ul')
lis=ul.find_all('li')
for li in lis:
    href = li.a['href']
    name = li.a.get_text().strip()
    ggstart_time = li.find('span', class_='date').get_text()

    if 'http' in href:
        href = href
    else:
        href = 'http://www.hljggzyjyw.gov.cn'+href

    tmp = [name, ggstart_time,href]
    print(tmp)

driver.quit()




