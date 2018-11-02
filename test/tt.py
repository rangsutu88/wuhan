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
import requests

# def out(a):
#     def mid(f):
#         def inner(*args):
#             c=args[0]
#             print(c)
#
#             print(a)
#             print('装饰器')
#
#             return f(*args)
#         return inner
#     return mid
#
# @out(a=1)
# def func(b=2,num=3):
#     print('函数体')
#     print(b)
#
# func()

# driver=webdriver.Chrome()
# driver.get('https://www.baidu.com/')


def out(f):
    def inner(*args):
        print(args)
        driver=args[0]

        print(driver)
        print('装饰器')
        return f(*args)

    return inner
@out
def fun(num=1,cnum=2):

    # print(num)
    # print(cnum)
    print('函数体')



fun(3,4)
# driver.quit()