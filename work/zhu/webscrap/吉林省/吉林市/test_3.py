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

PAGE = []
CC_TEXT=[]
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




for i in range(1,7):



    if i != 1:
        driver.find_element_by_xpath('//div[@class="ewb-right-hd"]/a[4]').click()
        locator=(By.XPATH,'//div[@id="categorypagingcontent"]/div[1]/div[1]/a')
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath('//div[@id="categorypagingcontent"]/div[{}]/div[1]/a'.format(i)).click()

        locator=(By.XPATH,'//*[@id="categorypagingcontent"]/div/div/div[2]')
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    try:
        page = driver.find_element_by_xpath('//li[@class="wb-page-li"][last()-1]/a').text
        total_ = re.findall('/(\d+)', page)[0]
    except:
        html=driver.page_source
        if '本栏目暂无信息' in html:
            total_=0
        else:
            total_=1
    cc_text=driver.find_element_by_xpath('//div[@class="ewb-right-hd"]/span').text
    PAGE.append(total_)
    CC_TEXT.append(cc_text)

print(PAGE)
print(CC_TEXT)



#获取总页数

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

