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
driver.get('http://www.bzztb.gov.cn/BZWZ/jyxx/003001/003001004/003001004001/003001004001001/')

#第一个等待
locator=(By.XPATH,'(//*[@id="MoreInfoList1_moreinfo"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]/a)|(//*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a)')

WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url



print(url)
#获取总页数
PAGE=[]
#
total = 0
for i in range(1,6):

        if i == 1:
            val = driver.find_element_by_xpath(
                '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a').text
            try:
                driver.execute_script("ShowNewPage('moreinfo.aspx?Paging=2');")
            except:
                driver.execute_script("window.location.href='./moreinfo.aspx?Paging=2'")

            locator = (By.XPATH,
                       '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a[not(contains(string(),"{}"))]'.format(
                           val))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


        elif i == 2:
            i = 2
            j = 2
            val = driver.find_element_by_xpath(
                '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a').text

            driver.find_element_by_xpath(
                '(//font[@color="red"])[1]/../../../following-sibling::tr[1]/td/table/tbody/tr[{}]/td/table/tbody/tr[{}]/td/a'.format(
                    i, j)).click()
            time.sleep(1)


            try:
                driver.execute_script("ShowNewPage('moreinfo.aspx?Paging=2');")
            except:
                driver.execute_script("window.location.href='./moreinfo.aspx?Paging=2'")
            locator = (By.XPATH,
                       '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a[not(contains(string(),"{}"))]'.format(
                           val))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        elif i > 2:
            val = driver.find_element_by_xpath(
                '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a | //*[@id="main"]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/a').text

            driver.find_element_by_xpath(
                '(//font[@color="red"])[1]/../../../following-sibling::tr[1]/td/table/tbody/tr[{}]/td/a'.format(
                    i)).click()
            time.sleep(1)

            try:
                driver.execute_script("ShowNewPage('moreinfo.aspx?Paging=1');")
            except:
                driver.execute_script("window.location.href='./moreinfo.aspx?Paging=1'")
            locator = (By.XPATH,
                       '//td[@align="right"]/table/tbody/tr[1]/td/table/tbody/tr/td[last()-1]/a[not(contains(string(),"{}"))]'.format(
                           val))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

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

