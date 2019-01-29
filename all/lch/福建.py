import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from PIL import Image, ImageEnhance
import pytesseract
import PIL.ImageOps


from zhulong.util.etl import est_tbs,est_meta,est_html,gg_existed,est_gg

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]
#
#
url="http://czj.dg.gov.cn/dggp/portal/topicView.do?method=view&id=1660"
driver=webdriver.Chrome()
driver.maximize_window()
driver.get(url)


locator = (By.XPATH, '//tbody[@class="tableBody"]/tr[1]//a')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
select=Select(driver.find_element_by_xpath('//select[@name="__ec_pages"]'))
select.select_by_value('10')
time.sleep(2)
driver.save_screenshot('f.png')
img=driver.find_element_by_xpath('//img[@class="yzmimg y"]')
location=img.location
print(location)
size=img.size
print(size)
rangle=(int(location['x']),int(location['y']),
        int(location['x']+size['width']),int(location['y']+size['height']))
print(rangle)
i = Image.open('f.png')
verifycodeimage = i.crop(rangle)
verifycodeimage.save('f2.png')
im = Image.open('f2.png')#验证码区域


def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table
im = im.convert('L')#转换为灰色图像
# im.show()
binaryImage = im.point(initTable(), '1')
# binaryImage.show()


im1 = binaryImage.convert('L')

im2 = PIL.ImageOps.invert(im1)
im3 = im2.convert('1')
im4 = im3.convert('L')


box = (50, 20, 570, 170)
region = im4.crop(box) # 将图片字符放大
out = region.resize((1200, 380))
# out = im4.resize((1200, 380))

out.show()
code = pytesseract.image_to_string(out)  # 读取里面的内容
code=code.replace(' ','')
driver.quit()
print(code)

"""
name	name	    extension名称
version	text	    版本名称
installed	bool	如果当前安装了此版本的此扩展，则为True布尔
superuser	bool	如果只允许超级用户安装此扩展，则为True
relocatable	bool	如果扩展可以重定位到另一个模式，则为True
schema	name	    必须安装扩展的模式的名称，如果部分或完全可重定位，则为NULL
requires	name[]	先决条件扩展名称，如果没有，则为NULL
comment	text	    扩展程序控制文件中的注释字符串

"""

"""
分机名称
版本名称
如果当前安装了此版本的此扩展，则为True布尔	
如果只允许超级用户安装此扩展，则为True
如果扩展可以重定位到另一个模式，则为True
必须安装扩展的模式的名称，如果部分或完全可重定位，则为NULL
先决条件扩展名称，如果没有，则为NULL
扩展程序控制文件中的注释字符串
"""
