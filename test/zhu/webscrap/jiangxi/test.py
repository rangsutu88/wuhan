from selenium import webdriver

# from selenium import webdriver
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def go():
    driver=webdriver.Chrome()
    driver.get('http://www.jxsggzy.cn/web/jyxx/002006/002006001/3261.html')
    title=driver.title
    print(title)
    if title=='404 Not Found':
        data=[]
        tmp = [None,None,None]
        data.append(tmp)
        df = pd.DataFrame(data=data)
        return df
    locator=(By.XPATH,'//*[@id="gengerlist"]/div[1]/ul/li[1]/a')
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    driver.quit()

a=go()
print(a)
