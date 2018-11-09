import pandas as pd
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lmfscrap import web


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="http://ggzyjy.ntzw.gov.cn/jyxx/tradeInfo.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


def f1(driver, num):
    locator = (By.XPATH, "//tbody[@id='xxList']/tr[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, "//span[@class='pg_maxpagenum']")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    cnum = int(driver.find_element_by_xpath("//span[@class='pg_maxpagenum']").text.split("/")[0])

    val = driver.find_element_by_xpath("//tbody[@id='xxList']/tr[1]//a").get_attribute("href")
    val = val[-20:]
    # print(val)
    if cnum != num:
        locator = (By.CLASS_NAME, "pg_num_input")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        time.sleep(1.5)
        input = driver.find_element_by_class_name("pg_num_input")
        print(input)
        input.clear()
        input.send_keys(num)
        driver.find_element_by_class_name("pg_gobtn").click()

        locator = (By.XPATH, "//tbody[@id='xxList']/tr[1]//a[not(contains(@href,'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []
    page = driver.page_source

    soup = BeautifulSoup(page, "lxml")

    tb = soup.find("tbody", id="xxList")

    trs = tb.find_all("tr")

    for tr in trs:
        tmp = [td.text.strip() for td in tr.find_all("td")]
        a = tr.find("a")
        tmp.append("http://ggzyjy.ntzw.gov.cn" + a["href"])

        data.append(tmp)
    df = pd.DataFrame(data=data)
    df = df.iloc[:, 2:]
    return df


def f2(driver):
    locator = (By.XPATH, "//tbody[@id='xxList']/tr[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, "//span[@class='pg_maxpagenum']")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    cnum = int(driver.find_element_by_xpath("//span[@class='pg_maxpagenum']").text.split("/")[1])
    driver.quit()
    return cnum


# def

def zhongbiaohx_gg(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@id='lefttree']/li[contains(string(),'建设工程')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath("//ul[@id='lefttree']/li[contains(string(),'建设工程')]").click()

        locator = (By.XPATH, "//ul[@class='ewb-menu-items']/li[contains(string(),'中标候选人公示')]")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
        driver.find_element_by_xpath("//ul[@class='ewb-menu-items']/li[contains(string(),'中标候选人公示')]").click()
        return f(*krg)

    return wrap


def general_template(tb, url, col, f, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f(f1),
        "f2": f(f2),
        "tb": tb,
        "col": col,
        "conp": conp,
        "num":10,
        "total": 10

    }
    m = web()
    m.write(**setting)


conp = ["testor", "zhulong", "192.168.3.171", "test", "public"]

data = [
    ["zhongbiaohx_gg_test", "http://ggzyjy.ntzw.gov.cn/jyxx/tradeInfo.html",
     ["gctype", "zbfs", "title", "city", "ggstart_time", "href"], zhongbiaohx_gg]

]
for w in data:
    general_template(w[0], w[1], w[2], w[3], conp)
