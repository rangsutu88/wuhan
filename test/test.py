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
driver.get('http://www.dyggzy.com/categoryList_3cc01e2ead9e420db555915f5c7ae233.html')

# 第一个等待
locator = (By.XPATH, '//*[@id="parent_center1-1"]/span')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
url = driver.current_url

# 寻找当前页
cnum=driver.find_element_by_xpath('//li[@class="ewb-page-li current"]').text.strip()
print(cnum)

# cnum = re.findall('-(\d+?)\.html', url)[0]
# print(cnum)
main_url = url.rsplit('/', maxsplit=1)[0]
print(main_url)

# 第二个等待
val = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/ul/li[1]/div/a').text
print(val)

# 翻页

# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")

# 翻页

driver.get('http://www.gyggzy.gov.cn/ggfwpt/012001/012001001/2.html')

# 第二个等待
locator = (By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/ul/li[1]/div/a[not(contains(string(),"%s"))]' % val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

while True:
    val = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/ul/li[1]/div/a').text
    driver.find_element_by_xpath('//li[@class="ewb-page-li "][last()]').click()
    locator = (By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/ul/li[1]/div/a[not(contains(string(),"%s"))]' % val)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    val = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/ul/li[1]/div/a').text
    dr=driver.find_element_by_xpath('//li[@class="ewb-page-li ewb-page-hover"][last()]')
    try:
        dr.find_element_by_tag_name('a').click()
        locator = (By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/ul/li[1]/div/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        total=driver.find_element_by_xpath('//li[@class="ewb-page-li current"]').text
        print(total)
        break


# page = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[3]/div[2]/a[4]').get_attribute('href')
#
# total = re.findall('-(\d+?)\.html', page)[0]
# total = int(total)
# print(total)







# data = []
#
# html = driver.page_source
# soup = BeautifulSoup(html, 'lxml')
# div = soup.find('div', class_='lb_ul')
# lis = div.find_all('li')
# for li in lis:
#     href = li.a['href']
#     name = li.a.span.get_text()
#     ggstart_time = li.find('span', class_='sp2').get_text()
#
#     if 'http' in href:
#         href = href
#     else:
#         href = None
#
#     tmp = [name, href, ggstart_time]
#     print(tmp)

# time.sleep(5)
driver.quit()




