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
driver.get('http://www.jl.gov.cn/ggzy/zfcg/cggg/')

# 第一个等待
locator = (By.XPATH, '//ul[@id="demoContent"]/li/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
url = driver.current_url

# 寻找当前页
cnum=driver.find_element_by_xpath('//div[@id="pages"]/span').text.strip()
# print(cnum)

print(cnum)
num=2

print(url)

# 第二个等待
val = driver.find_element_by_xpath('//ul[@id="demoContent"]/li/a').text
print(val)

# 翻页

driver.find_element_by_xpath('//div[@id="pages"]/a[last()]').click()

# 翻页

# driver.get(url)

# 第二个等待
locator = (By.XPATH, '//ul[@id="demoContent"]/li/a[not(contains(string(),"%s"))]' % val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f2(driver):
    locator = (By.XPATH, '//ul[@id="demoContent"]/li/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    while True:
        try:
            val = driver.find_element_by_xpath('//ul[@id="demoContent"]/li/a').text
        except:
            val='none'

        driver.find_element_by_xpath('//div[@id="pages"]/a[last()-1]').click()
        try:
            locator = (By.XPATH, '//ul[@id="demoContent"]/li/a[not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(5)


        text=driver.find_element_by_xpath('//div[@id="pages"]/a[last()]').text
        if text !='下一页>':
            page=driver.find_element_by_xpath('//div[@id="pages"]/span').text.strip()
            break

    total = int(page)


    return total

page=f2(driver)
print(page)

# page = driver.find_element_by_xpath('//div[@class="yahoo2"]/div/span/b[2]').text
#
# page=re.findall('/(\d+)',page)[0]
# total = int(page)
# print(total)
url=driver.current_url
data = []

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div = soup.find('ul', id='demoContent')
divs = div.find_all('li')

for li in divs:
    href=li.a['href']
    name=li.a.get_text()
    address=li.find('span',class_='arealeft').get_text()
    ggstart_time=li.find('span',class_='ewb-list-date').get_text()
    if 'http' in href:
        href=href
    else:
        href='http://www.jl.gov.cn'+href

    tmp = [name, ggstart_time,href,address]
    print(tmp)



driver.quit()




