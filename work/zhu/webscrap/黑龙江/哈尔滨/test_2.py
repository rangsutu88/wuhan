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
driver.get('http://113.6.234.4/Bid_Front/ZBMore.aspx?t=%u5168%u90e8')

# 第一个等待
locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
url = driver.current_url

# 寻找当前页
cnum=driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[last()]/td/table/tbody/tr/td/span').text.strip()
# print(cnum)

print(cnum)
num=2

print(url)

# 第二个等待
val = driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a').text
print(val)

# 翻页

driver.execute_script("javascript:__doPostBack('GV_Data','Page${}')".format(num))

# 翻页

# driver.get(url)

# 第二个等待
locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f2(driver):
    locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    while True:
        val = driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a').text
        driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[last()]/td/table/tbody/tr/td[last()]').click()
        locator = (By.XPATH, '//*[@id="GV_Data"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        try:
            driver.find_element_by_xpath('//*[@id="GV_Data"]/tbody/tr[last()]/td/table/tbody/tr/td[last()]/a')
        except:
            total = driver.find_element_by_xpath(
                '//*[@id="GV_Data"]/tbody/tr[last()]/td/table/tbody/tr/td[last()]').text
            break
    total = int(total)


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
div = soup.find('table', id='GV_Data')
divs = div.find_all('tr',style="height:22px;")



for li in divs:
    tds=li.find_all('td')
    href_ = tds[1].a['href']
    name = tds[1].a.get_text()
    ggstart_time = tds[2].get_text()
    click_num =tds[3].get_text()
    driver.execute_script(href_)
    WebDriverWait(driver,10).until(lambda driver:'TenderContent' in driver.current_url)
    href=driver.current_url
    driver.back()

    tmp = [name, ggstart_time,href,click_num]
    print(tmp)



driver.quit()




