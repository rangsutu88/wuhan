import random
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
import requests
import json
from fake_useragent import UserAgent
from multiprocessing import Queue


from zhulong.util.etl import est_tbs,est_meta,est_html,gg_existed,est_gg


q=Queue()
for i in range(10):
    q.put(i)
print(q.get())
print(q.get())
print(q.get())