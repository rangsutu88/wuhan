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
driver.get('http://218.65.3.188/rcs/cjxx/zfcgyztb/index.htm')

# 第一个等待
locator = (By.XPATH, '/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[3]/tbody/tr[2]/td[1]/div')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
url = driver.current_url

# 寻找当前页
cnum=driver.find_element_by_xpath('/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[5]/tbody/tr/td/div').text
cnum=re.findall('当前第(\d+)页',cnum)[0]
print(cnum)
# cnum = re.findall('-(\d+?)\.html', url)[0]
# print(cnum)
main_url = url.rsplit('/', maxsplit=1)[0]
print(main_url)

# 第二个等待
val = driver.find_element_by_xpath('/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[3]/tbody/tr[2]/td[1]/div').text
print(val)

# 翻页

# driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','2')")

# 翻页

# driver.get('http://218.65.3.188/rcs/cjxx/zfcgyztb/index_1.htm')

# 第二个等待
locator = (By.XPATH, '/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[3]/tbody/tr[2]/td[1]/div[not(contains(string(),"%s"))]' % val)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

# 获取总页数
page = driver.find_element_by_xpath('/html/body/table[4]/tbody/tr/td[3]/div/table[4]/tbody/tr/td/div/table[5]/tbody/tr/td/div').text

total = re.findall('总共(\d+?)页', page)[0]
# total = int(total)
print(total)

data = []

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
trs=soup.find_all('tr',bgcolor='#FFFFFF')
print(len(trs))
for i in range(1,len(trs)):
    tr=trs[i]
    tds=tr.find_all('td')
    index_num=tds[0].div.get_text()
    index_num=re.findall("xxsqh=\'(.+?)\';",index_num)[0]

    status=tds[1].div.div.get_text()
    href=tds[2].div.div.a['href'].strip('.')
    name=tds[2].div.div.a.get_text()
    ggsj=tds[3].div.div.get_text()
    mxdx=tds[4].div.div.get_text()
    ggstart_time=tds[5].div.div.get_text()





    if 'http' in href:
        href = href
    else:
        href = main_url+href
    #
    # tmp = [index_num]
    tmp = [index_num,status,ggsj,mxdx,name, href, ggstart_time]
    print(tmp)

driver.quit()




