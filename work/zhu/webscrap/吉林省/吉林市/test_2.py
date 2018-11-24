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
driver.get('http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001001/003001001001/')
# except:
    # driver.execute_script('javascript:window.stop()')

#第一个等待
locator=(By.XPATH,'//ul[@class="ewb-com-items"]/li[1]/div/a')
WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
url=driver.current_url


#寻找当前页
cnum=driver.find_element_by_xpath('//li[@class="wb-page-li"][last()-1]/a').text.strip()
# print(cnum)
cnum=re.findall('(\d+)/',cnum)[0]
print(cnum)




#第二个等待
val=driver.find_element_by_xpath('//ul[@class="ewb-com-items"]/li[1]/div/a').text
print(val)

#翻页
num=2
driver.execute_script("ShowAjaxNewPage(window.location.pathname,'categorypagingcontent',{})".format(num))



#第二个等待
locator = (By.XPATH, '//ul[@class="ewb-com-items"]/li[1]/div/a[not(contains(string(),"%s"))]'%val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

#获取总页数
page=driver.find_element_by_xpath('//li[@class="wb-page-li"][last()-1]/a').text
print(page)
total=re.findall('/(\d+)',page)[0]
total=int(total)
print(total)

data=[]

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
div=soup.find('ul',class_='ewb-com-items')
trs=div.find_all('li')

for tr in trs:
    href=tr.div.a['href']
    name=tr.div.a.get_text()
    ggstart_time=tr.span.get_text().strip()

    if 'http' in href:
        href=href
    else:
        href='http://www.jlsggzyjy.gov.cn'+href

    tmp = [name, ggstart_time, href]

    print(tmp)


driver.quit()

