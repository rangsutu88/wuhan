

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


# #初始化
# driver=webdriver.Chrome()
# driver.get('http://www.qhggzyjy.gov.cn/ggzy/jyxx/001002/secondPage.html')
#
# #第一个等待
# locator=(By.XPATH,'//table[@class="ewb-info-table"]/tbody/tr[1]/td[2]/a')
# WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# url=driver.current_url
# driver.switch_to.frame()



