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

driver=webdriver.Chrome()
driver.get('http://www.jxsggzy.cn/web/jyxx/002001/002001001/120.html')
# time.sleep(2)
# # locator=(By.XPATH,'//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
# # WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# num=10
# # locator=(By.XPATH,'//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b')
# # WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
# page_all=driver.find_element_by_xpath('//*[@id="index"]').text.split('/')[1]
# print(page_all)
# url=driver.current_url
# cnum=int(re.findall("/([0-9]{1,}).html",url)[0])
# s="/%d.html"%(num)
# url=re.sub("/[0-9]{1,}.html",s,url)
# print(cnum)
# print(url)
# # driver.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$myGV$ctl23$LinkButtonNextPage','')")
# # time.sleep(4)
# # page_all=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_myGV_ctl23_LabelPageCount"]').text
# # print(page_all)
# # time.sleep(4)
# ht=driver.page_source
# soup=BeautifulSoup(ht,'lxml')
# uls = soup.find('div',class_="ewb-infolist")
# lis=uls.find_all('li')
# for li in lis:
#     title=li.a.get_text()
#     href=li.a['href']
#     href='http://www.jxsggzy.cn'+href
#     date_time=li.span.get_text()
#     tmp=[title,href,date_time]
#     # print(tmp)
#
#
# driver.get(url)
# driver.quit()
try:
    driver.get('http://www.jxsggzy.cn/web/jyxx/002001/002001001/640.html')
except:
    print('cucuo')
