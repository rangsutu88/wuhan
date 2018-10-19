import os
import pymongo
import time
import re
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymysql import connect



DB_NAME=os.path.basename(__file__).split('.')[0]

MAIN_URL='http://www.whzbtb.cn/V2PRTS/'

def get_content(driver):
    HTML=driver.page_source
    tree=etree.HTML(HTML)
    tables=tree.xpath("//table[@class='datagrid-btable']/tbody/tr")
    for i in range(0,len(tables)//2):
        content_dict = {}
        tr=tables[i]
        datagrid=tr.xpath('./td[1]/div/text()')[0]
        tenderPrjName_link= None if  tr.xpath('./td[2]/div/a/@onclick')==[] else tr.xpath('./td[2]/div/a/@onclick')[0]
        tenderPrjName=None if tr.xpath('./td[2]/div/a/text()')==[] else tr.xpath('./td[2]/div/a/text()')[0]
        noticeState= None if tr.xpath('string(./td[3]/div)')=='' else tr.xpath('string(./td[3]/div)')

        tr=tables[i+len(tables)//2]
        registrationId = None if  tr.xpath('./td[1]/div/text()')==[] else tr.xpath('./td[1]/div/text()')[0]
        prjbuildCorpName = None if tr.xpath('./td[2]/div/text()')==[] else tr.xpath('./td[2]/div/text()')[0]
        noticeStartDate = None if  tr.xpath('./td[3]/div/text()') == [] else tr.xpath('./td[3]/div/text()')[0]
        noticeEndDate = None if tr.xpath('./td[4]/div/text()') == [] else tr.xpath('./td[4]/div/text()')[0]
        totalInvestment = None if tr.xpath('./td[5]/div/text()') == [] else tr.xpath('./td[5]/div/text()')[0]
        platformDataSourceName = None if tr.xpath('./td[6]/div/text()') == [] else tr.xpath('./td[6]/div/text()')[0]
        evaluationMethodName = None if tr.xpath('./td[7]/div/text()') == [] else tr.xpath('./td[7]/div/text()')[0]
        tenderPrjName_link=MAIN_URL+re.findall(r"'.+'",tenderPrjName_link)[0].strip(r"'")

        try:
            content_two=callback_parse(tenderPrjName_link)
        except:
            content_two=None
            print('获取{}详细页失败'.format(tenderPrjName_link))

        content_dict['datagrid']=datagrid
        content_dict['tenderPrjName_link']=tenderPrjName_link
        content_dict['tenderPrjName']=tenderPrjName
        content_dict['noticeState']=noticeState
        content_dict['registrationId']=registrationId
        content_dict['prjbuildCorpName']=prjbuildCorpName
        content_dict['noticeStartDate']=noticeStartDate
        content_dict['noticeEndDate']=noticeEndDate
        content_dict['totalInvestment']=totalInvestment
        content_dict['platformDataSourceName']=platformDataSourceName
        content_dict['evaluationMethodName']=evaluationMethodName
        content_dict['two_content']='%r'%content_two
        # print(content_dict)


        db.insert_db(content_dict)




def callback_parse(url):
    cookie=driver.get_cookies()
    cookies = {}
    for i in cookie:
        cookies['{}'.format(i['name'])] = i['value']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',

    }

    req=requests.get(url,headers=headers,cookies=cookies,timeout=4).text
    soup=BeautifulSoup(req,'lxml')
    content=soup.find_all('div',class_='trading_publicly_fr fr')[0]
    return content


# def callback_parse():
#     handles=driver.window_handles
#     driver.switch_to_window(handles[1])
#     time.sleep(0.5)
#     page=driver.find_element_by_xpath('//div[@class="pageWap_box"]')
#     driver.close()
#     driver.switch_to_window(handles[0])
#     return page


def change_page(driver):
    time.sleep(0.5)
    page_all=driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[8]/span').text
    page=re.findall('共(\d+)页',page_all)[0]
    print(page_all)

    for i in range(656,int(page)+1):
        print('正在爬取第{}页数据'.format(i))
        # try:
            # get_content(driver)
        # except:
            # print('出现异常,请调试代码')

        driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[7]/input').clear()
        driver.find_element_by_xpath('//div[@class="datagrid-pager pagination"]/table/tbody/tr/td[7]/input').send_keys(i,Keys.ENTER)

        WebDriverWait(driver,30).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="datagrid-row-r1-1-9"]/td[1]/div'),str(i*10)))
        get_content(driver)


class To_db():
    def __init__(self):
        self.conn=pymongo.MongoClient(host='127.0.0.1',port=27017)
    def create_db(self):
        self.db=self.conn['wuhan']
        self.collections=self.db['{}'.format(DB_NAME)]
    def insert_db(self,dict_c):
        self.collections.insert_one(dict_c)
    def close_db(self):
        self.conn.close()



if __name__ == '__main__':
    db=To_db()
    db.create_db()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver=webdriver.Chrome()
    driver.implicitly_wait(10)
    url = 'http://www.whzbtb.cn/V2PRTS/TendererNoticeInfoListInit.do'
    driver.get(url)
    change_page(driver)


    db.close_db()
    driver.close()
    driver.quit()