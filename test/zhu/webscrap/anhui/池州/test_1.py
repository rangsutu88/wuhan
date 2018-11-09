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
driver.get('http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001001/002001001001/')

#第一个等待
locator=(By.XPATH,'//li[@class="wb-data-list"][1]/div/a')

WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url



print(url)
#获取总页数
PAGE=[]
#
total = 0
for i in range(1,6):

    if i != 1:
        driver.find_element_by_xpath('(//font[@color="#17a8e4"])/../../../following-sibling::tr[1]/td/table/tbody/tr[2]/td/a').click()
        locator=(By.XPATH,'(//h4[@class="s-block-title"])[1]/a[2]')
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath('(//h4[@class="s-block-title"])[{}]/a[2]'.format(i-1)).click()
        locator=(By.XPATH,'//div[@id="Paging"]')
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    try:
        page = driver.find_element_by_xpath('//td[@class="huifont"]').text
        total_ = re.findall(r'/(\d+)', page)[0]
    except:
        total_=0

    print(total_)
    PAGE.append(total_)
    total = total + int(total_)


print(total)


driver.quit()

