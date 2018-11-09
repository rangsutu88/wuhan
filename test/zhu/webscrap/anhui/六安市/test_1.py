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
driver.get('http://www.laztb.gov.cn/laztb/jyxx/002007/002007001/002007001001/')

try:
    driver.switch_to.frame(1)
except:
    pass
#第一个等待
locator=(By.XPATH,'//li[@class="ewb-plate-list clearfix"]/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

driver.switch_to.parent_frame()
url=driver.current_url

c_type=driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[4]').text.strip()
c_text=driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[3]').text.strip()
print(c_text,c_type)

print(url)
driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[2]').click()
locator=(By.XPATH,'/html/body/div[3]/div[2]/div[2]/div/div[1]/div/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

html=driver.page_source
soup=BeautifulSoup(html,'lxml')
lis=soup.find_all('li',class_='wb-tree-items haschild')
print(len(lis))
#获取总页数
PAGE=[]
CC_TEXT=[]
#
total = 0
for i in range(1,len(lis)+1):

    driver.find_element_by_xpath('//li[@class="wb-tree-items haschild"][{}]'.format(i)).click()
    time.sleep(0.1)
    driver.find_element_by_xpath('//li[@class="wb-tree-items haschild current"]/ul/li/a[contains(string(),"{c_type}")]'.format(c_type=c_type)).click()

    locator = (By.XPATH, '//font[@class="currentpostionfont01"]/../font[2]/a[4]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    try:
        driver.switch_to.frame(1)
    except:
        pass
    try:
        page = driver.find_element_by_xpath('//td[@class="huifont"]').text
        total_ = re.findall(r'/(\d+)', page)[0]
    except:
        total_=0
    driver.switch_to.parent_frame()
    c_text = driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[3]').text.strip()


    # print(total_)
    print(i)

    if i != len(lis)+1:
        driver.find_element_by_xpath('//font[@class="currentpostionfont01"]/../font[2]/a[2]').click()
        locator = (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div[1]/div/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    PAGE.append(total_)
    CC_TEXT.append(c_text)
    total = total + int(total_)


print(PAGE)
print(CC_TEXT)


driver.quit()

