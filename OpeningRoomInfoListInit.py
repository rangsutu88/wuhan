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


def get_content(driver):
    HTML=driver.page_source
    tree=etree.HTML(HTML)
    tables=tree.xpath("//table[@class='datagrid-btable']/tbody/tr")

    for i in range(0,len(tables)//2):
        content_dict={}
        tr=tables[i]
        # datagrid=tr.xpath('./td[1]/div/text()')[0]
        openingName_link = tr.xpath('./td[2]/div/a/@onclick')[0]
        openingName = tr.xpath('./td[2]/div/a/text()')[0]
        openingPlace=tr.xpath('./td[3]/div/text()')[0]
        openingName_link=MAIN_URL+re.findall(r"'.+'",openingName_link)[0].strip(r"'")

        tr=tables[i+len(tables)//2]
        openingTypeName = tr.xpath('./td[1]/div/text()')[0]
        reserveStartTime =None if  tr.xpath('./td[2]/div/text()')==[] else tr.xpath('./td[2]/div/text()')[0]
        reserveEndTime = None if  tr.xpath('./td[3]/div/text()')==[] else tr.xpath('./td[3]/div/text()')[0]
        departName = tr.xpath('./td[4]/div/text()')[0]
        name = tr.xpath('./td[5]/div/text()')[0]
        address = tr.xpath('./td[6]/div/text()')[0]

        try:
            content_two=callback_parse(openingName_link)
        except:
            content_two=None
            print('获取{}详情页失败'.format(openingName_link))

        content_dict['openingName_link']=openingName_link
        content_dict['openingName']=openingName
        content_dict['openingPlace']=openingPlace
        content_dict['openingTypeName']=openingTypeName
        content_dict['reserveStartTime']=reserveStartTime
        content_dict['reserveEndTime']=reserveEndTime
        content_dict['departName']=departName
        content_dict['name']=name
        content_dict['address']=address
        content_dict['content_two']='%r'%content_two
        db.insert_db(content_dict)

        # print(content_dict)

def callback_parse(url):
    cookie=driver.get_cookies()
    cookies = {}
    for i in cookie:
        cookies['{}'.format(i['name'])] = i['value']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }

    req=requests.get(url,headers=headers,cookies=cookies).text
    soup=BeautifulSoup(req,'lxml')
    content=soup.find_all('div',class_='trading_publicly_fr fr')[0]
    return content


def change_page(driver):
    time.sleep(0.5)

    page_all=driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[8]/span').text
    page=re.findall('共(\d+)页',page_all)[0]
    print(page_all)
    pages=driver.find_element_by_xpath("//div[@class='pagination-info']").text
    print(pages)

    for i in range(12,int(page)+1):
        print('正在爬取第{}页数据'.format(i))
        driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[7]/input').clear()
        driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[7]/input').send_keys(i,Keys.ENTER)


        if i != page_all:
            WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="datagrid-row-r1-1-9"]/td[1]/div'),str(i*10)))
        else:
            time.sleep(1)

        try:
            get_content(driver)
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
    url = 'http://www.whzbtb.cn/V2PRTS/OpeningRoomInfoListInit.do'
    driver.get(url)
    change_page(driver)


    db.close_db()
    driver.close()
    driver.quit()
#finish_all