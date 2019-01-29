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
driver.get('http://ggzy.wlmq.gov.cn/generalpage.do?method=showList&fileType=201605-043&faname=201605-038&num=4')

locator = (By.XPATH, '//table[@id="packTable"]//tr[2]/td[1]/a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

cnum = driver.find_element_by_xpath('//nobr[@id="packTableRowCount"]').text.strip()
cnum = re.findall('显示(.+)到', cnum)[0]
cnum = int(cnum) // 15 + 1

for num in range(1,10):

    if int(cnum) != num:

        val = driver.find_element_by_xpath('//table[@id="packTable"]//tr[2]/td[1]/a').get_attribute('onclick')[-34:-2]
        print(val)

        driver.execute_script("TabAjaxQuery.gotoPage({},'packTable');".format(num))

        locator = (By.XPATH, '//table[@id="packTable"]//tr[2]/td[1]/a[not(contains(@onclick,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        # time.sleep(20)

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.find('table', id='packTable').find_all('tr')

    for i in range(1, len(lis)):
        li = lis[i]

        tds = li.find_all('td')
        href = tds[0].a['onclick']
        href = re.findall("this,\'(.+)\'", href)[0]
        name = tds[0].a['title']
        ggstart_time = tds[1].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://ggzy.wlmq.gov.cn/infopublish.do?method=infoPublishView&infoid=' + href

        tmp = [name,  ggstart_time,href]
    print(tmp)
driver.quit()

