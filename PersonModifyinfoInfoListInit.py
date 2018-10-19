import os
import time
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from connect_mongo import To_db

DB_NAME=os.path.basename(__file__).split('.')[0]
MAIN_URL='http://www.whzbtb.cn/V2PRTS/'


def get_content():
    HTML=driver.page_source
    tree=etree.HTML(HTML)
    tables=tree.xpath("//table[@class='datagrid-btable']/tbody/tr")

    for i in range(0,len(tables)//2):
        content_dict={}
        tr=tables[i]
        # datagrid=tr.xpath('./td[1]/div/text()')[0]
        personBasicinfoName=None if  tr.xpath('./td[2]/div/text()')==[] else tr.xpath('./td[2]/div/text()')[0]

        tr=tables[i+len(tables)//2]
        insertDate = tr.xpath('./td[1]/div/text()')[0]
        oldCorpName =None if tr.xpath('./td[2]/div/text()')==[] else tr.xpath('./td[2]/div/text()')[0]

        corpName = None if  tr.xpath('./td[3]/div/text()')==[] else tr.xpath('./td[3]/div/text()')[0]
        personModifyMark = tr.xpath('./td[4]/div/text()')[0]

        content_dict['personBasicinfoName']=personBasicinfoName
        content_dict['insertDate']=insertDate
        content_dict['oldCorpName']=oldCorpName
        content_dict['corpName']=corpName
        content_dict['personModifyMark']=personModifyMark
        db.insert_db(content_dict)

        # print(content_dict)



def change_page():
    time.sleep(0.5)
    page_all=driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[8]/span').text
    page=re.findall('共(\d+)页',page_all)[0]
    print(page_all)
    # pages = driver.find_element_by_xpath("//div[@class='pagination-info']").text
    # print(pages)

    for i in range(1,int(page)+1):
        print('正在爬取第{}页数据'.format(i))
        driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[7]/input').clear()
        driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[7]/input').send_keys(i,Keys.ENTER)

        # time.sleep(10)
        WebDriverWait(driver,30).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="datagrid-row-r1-1-9"]/td[1]/div'),str(i*10)))
        try:
            get_content()
        except:
            print('出现异常,请调试代码')


if __name__ == '__main__':
    db=To_db()
    db.create_db(DB_NAME)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # driver=webdriver.Chrome()
    driver.implicitly_wait(10)
    url = 'http://www.whzbtb.cn/V2PRTS/PersonModifyinfoInfoListInit.do'
    driver.get(url)
    change_page()

    db.close_db()
    driver.close()
    driver.quit()
#finish_all