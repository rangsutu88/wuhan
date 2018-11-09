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
driver.get('http://zw.hainan.gov.cn/ggzy/syggzy/GGjxzbgs1/index.jhtml')

# 第一个等待
locator = (By.XPATH, '/html/body/div/div[7]/div[3]/table/tbody/tr[1]/td[2]/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
url = driver.current_url

# 寻找当前页
cnum=driver.find_element_by_xpath('/html/body/div/div[7]/div[3]/table/tbody/tr[21]/td/div/div').text.strip()
cnum=re.findall('记录 (\d+?)\/',cnum)
print(cnum)

# cnum = re.findall('-(\d+?)\.html', url)[0]
# print(cnum)
main_url = url.rsplit('/', maxsplit=1)[1]
# print(main_url)
print('即将翻页')

for num in range(2,31):
# 第二个等待
    val = driver.find_element_by_xpath('/html/body/div/div[7]/div[3]/table/tbody/tr[1]/td[2]/a').text
    # print(val)

    # 翻页

    driver.execute_script("location.href=encodeURI('index_{}.jhtml');".format(num))

    # 翻页

    # driver.get('http://www.gyggzy.gov.cn/ggfwpt/012001/012001001/2.html')

    # 第二个等待
    locator = (By.XPATH, '/html/body/div/div[7]/div[3]/table/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    one=driver.find_element_by_xpath('/html/body/div/div[7]/div[3]/table/tbody/tr[1]/td[2]/a').text
    print(one)





driver.quit()




