import pandas as pd  
import re 

from selenium import webdriver 
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

import sys 
import time
import json


from zhulong_.util.etl import gg_meta,gg_html


# driver=webdriver.Chrome()

# url="""http://ggzy.shaoyang.gov.cn/newsList.html?index=5&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xtype=%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD"""

# driver.get(url)



def f1(driver,num):
    locator=(By.ID,"list")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    cnum=int(driver.find_element_by_xpath("//span[@class='cPageNum']").text)
    if cnum!=num:
        #val=driver.find_element_by_xpath("//ul[@id='list']//li[2]//a").get_attribute("href")[-20:]

        driver.execute_script("pageNav.go(%d)"%num)

        time.sleep(0.2)
        locator=(By.CLASS_NAME,"h-load")
        WebDriverWait(driver,10).until(EC.invisibility_of_element_located(locator))

        # locator=(By.XPATH,"//ul[@id='list']//li[2]//a[not(contains(@href,'%s'))]"%val)
        # WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    page=driver.page_source

    soup=BeautifulSoup(page,"lxml")

    ul=soup.find("ul",id="list")

    lis=ul.find_all("li",recursive=False)[1:]
    data=[]
    for li in lis:
        a=li.find("a")
        span=li.find("span")
        name=a["title"]
        name=re.sub("【.*】","",name)
        href="http://ggzy.shaoyang.gov.cn"+a["href"]
        ggstart_time=span.text.strip()
        tmp=[name,href,ggstart_time]
        data.append(tmp)
    df=pd.DataFrame(data)
    return df 

def f2(driver):
    locator=(By.ID,"pageNav")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    try:
        total=int(re.findall('共([0-9]*)页',driver.find_element_by_id("pageNav").get_attribute("title"))[0])
    except StaleElementReferenceException:
        total=int(re.findall('共([0-9]*)页',driver.find_element_by_id("pageNav").get_attribute("title"))[0])
    total=int(total)
    driver.quit()
    return total
def f3(driver,url):


    driver.get(url)

    locator=(By.ID,"myFrame")

    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located(locator))
    driver.switch_to.frame(driver.find_element_by_id("myFrame"))
    before=len(driver.page_source)
    time.sleep(0.1)
    after=len(driver.page_source)
    i=0
    while before!=after:
        before=len(driver.page_source)
        time.sleep(0.1)
        after=len(driver.page_source)
        i+=1
        if i>5:break

    page=driver.page_source

    soup=BeautifulSoup(page,'lxml')

    div=soup.find('div',class_='content')

    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div


def switch_to(driver,xmtype,ggtype):
    locator=(By.ID,"list")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    cxmtype=driver.find_element_by_xpath("//div[@class='newsType on']").text
    if xmtype!=cxmtype:
        driver.find_element_by_xpath("//div[@class='newsType'][string()='%s']"%xmtype).click()
        time.sleep(0.2)
        locator=(By.CLASS_NAME,"h-load")
        WebDriverWait(driver,10).until(EC.invisibility_of_element_located(locator))

    cggtype=driver.find_element_by_xpath("//div[@class='site-bar']//button[@class='btn-site on']").text
    if ggtype!=cggtype:
        driver.find_element_by_xpath("//div[@class='site-bar']//button[string()='%s']"%ggtype).click()
        time.sleep(0.2)
        locator=(By.CLASS_NAME,"h-load")
        WebDriverWait(driver,10).until(EC.invisibility_of_element_located(locator))





def gcjs(f,xmtype,ggtype):
    def wrap(*krg):
        driver=krg[0]
        switch_to(driver,xmtype,ggtype)
        if f==f1:
            df=f(*krg)
            a={"xmtype":xmtype,"yuan_ggtype":ggtype}
            a=json.dumps(a,ensure_ascii=False)
            df["info"]=a
            return df 
        else:
            return f(*krg)
    return wrap

def zfcg(f,ggtype):
    def wrap(*krg):
        driver=krg[0]
        switch_to(driver,"政府采购",ggtype)
        if f==f1:
            df=f(*krg)
            a={"yuan_ggtype":ggtype}
            a=json.dumps(a,ensure_ascii=False)
            df["info"]=a
            return df 
        else:
            return f(*krg)
    return wrap


data=[

["gcjs_fangwushizheng_zhaobiao_gg","http://ggzy.shaoyang.gov.cn/newsList.html?index=5&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xtype=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE" 
,["name","href","ggstart_time","info"],gcjs(f1,"房建市政","招标公告"),gcjs(f2,"房建市政","招标公告")
]
,

["gcjs_shuili_zhaobiao_gg","http://ggzy.shaoyang.gov.cn/newsList.html?index=5&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xtype=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE" 
,["name","href","ggstart_time","info"],gcjs(f1,"水利工程","招标公告"),gcjs(f2,"水利工程","招标公告")
]
,

["gcjs_jiaotong_zhaobiao_gg","http://ggzy.shaoyang.gov.cn/newsList.html?index=5&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xtype=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE" 
,["name","href","ggstart_time","info"],gcjs(f1,"交通运输","招标公告"),gcjs(f2,"交通运输","招标公告")
]

,

["gcjs_tudi_zhaobiao_gg","http://ggzy.shaoyang.gov.cn/newsList.html?index=5&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xtype=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE" 
,["name","href","ggstart_time","info"],gcjs(f1,"土地开发整理","招标公告"),gcjs(f2,"土地开发整理","招标公告")
]


,

["gcjs_qita_zhaobiao_gg","http://ggzy.shaoyang.gov.cn/newsList.html?index=5&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xtype=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE" 
,["name","href","ggstart_time","info"],gcjs(f1,"其他","招标公告"),gcjs(f2,"其他","招标公告")
]


,

["zfcg_zhaobiao_gg","http://ggzy.shaoyang.gov.cn/newsList.html?index=5&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xtype=%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD" 
,["name","href","ggstart_time","info"],zfcg(f1,"采购公告"),zfcg(f2,"采购公告")
]

,

["zfcg_zhongbiaobiao_gg","http://ggzy.shaoyang.gov.cn/newsList.html?index=5&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xtype=%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD" 
,["name","href","ggstart_time","info"],zfcg(f1,"中标公示"),zfcg(f2,"中标公示")
]



]


#work_(conp=["postgres","since2015","127.0.0.1","hunan","shaoyang"],data=data[-1:],diqu="湖南省邵阳市")
#gg_meta(["postgres","since2015","127.0.0.1","hunan","shaoyang"],data,"湖南省邵阳市")

#gg(conp=["postgres","since2015","127.0.0.1","hunan","shaoyang"],diqu="湖南省邵阳市")
#["postgres","since2015","127.0.0.1","hunan","shaoyang"]
def work(conp):
    gg_meta(conp,data,"湖南省邵阳市")
    gg_html(conp,f3)

work(conp=["postgres","since2015","127.0.0.1","hunan","shaoyang"])