import requests


from bs4 import BeautifulSoup
import requests

url = 'http://2018.ip138.com/ic.asp'
proxies = {
    'http': 'http://220.186.132.51:37608',
    }
r = requests.get(url, proxies=proxies)
print(r)