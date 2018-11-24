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


#初始化
driver=webdriver.Chrome()
# driver.maximize_window()

# driver.set_page_load_timeout(3)
# try:
driver.get('http://www.ccggzy.gov.cn/qxxxgk/003002/003002001/CountyPurhcaseNotice.html')
# except:
    # driver.execute_script('javascript:window.stop()')

#第一个等待
locator=(By.XPATH,'//tbody[@id="showList"]/tr[1]/td[2]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url
PAGE=[]
CC_TEXT=[]
#
# for i in range(1,17):
#     if i != 1:
#         val = driver.find_element_by_xpath('//tbody[@id="showList"]/tr[1]/td[2]/a').text
#         driver.find_element_by_xpath('(//div[@class="ewb-screen-list"])[1]/span[{}]'.format(i)).click()
#         #
#         locator = (By.XPATH, '//tbody[@id="showList"]/tr[1]/td[2]/a[not(contains(string(),"%s"))]'%val)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
#         locator = (By.XPATH, '//span[@class="pg_maxpagenum"]')
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
#         time.sleep(0.5)
#     page = driver.find_element_by_xpath('//span[@class="pg_maxpagenum"]').text.strip()
#     cc_text=driver.find_element_by_xpath('//span[@class="ewb-screen-name current"]').text
#
#     print(page)
#     total_ = int(re.findall('/(\d+)', page)[0])
#     PAGE.append(total_)
#     CC_TEXT.append(cc_text)
# print(PAGE)
# print(CC_TEXT)
# print(sum(PAGE))
#
#
# #获取总页数
# page=driver.find_element_by_xpath('//span[@class="pg_maxpagenum"]').text
# print(page)
# total=re.findall('/(\d+)',page)[0]
# total=int(total)
# print(total)


data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('tbody',id='showList')
trs=div.find_all('tr')

for tr in trs:

    tds=tr.find_all('td')
    href=tds[1].a['href']
    name=tds[1].a.get_text().strip()

    if name.startswith('【'):
        gg_type=re.findall(r'^【(.+?)】',name)[0]
        name=name.split('】',maxsplit=1)[1]
    else:
        gg_type=None

    ggstart_time=tds[2].get_text()

    if 'http' in href:
        href=href
    else:
        href='http://www.ccggzy.gov.cn'+href

    tmp = [gg_type,name, ggstart_time, href]

    print(tmp)


driver.quit()

