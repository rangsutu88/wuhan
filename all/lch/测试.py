import requests
from pprint import pprint

from bs4 import BeautifulSoup
YEAR=[]
url='http://www.lczfcg.gov.cn/goods/publish/channel.jsp?Keyword=&Year=2019&Month=2&Area=&Channel=%B2%C9%B9%BA%B9%AB%B8%E6&Careful=&Fashion='
req=requests.get(url)
if req.status_code != 200:
    raise ValueError

# print(req.text)

soup=BeautifulSoup(req.text,'html.parser')

div = soup.find_all('td', attrs={"bgcolor": '#FFFFFF', "class": 'TD'})[1].find('table')
# if len(div) < 50:
#     print('nnn')

# print(div)
trs=div.find_all('tr',recursive=False)

print(len(trs))
""""""






