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


for i in range(0,len(trs),2):
    print()
    tr=trs[i]
    tds=tr.find_all('td',class_="TD")
    spans=tds[0].find_all('span')
    href=spans[0].a['href']
    if 'http' in href:
        href=href
    else:
        href="http://www.lczfcg.gov.cn/goods/publish/"+href
    name=spans[0].a.b.get_text().strip('.').strip()
    company=spans[1].get_text().strip()
    ggstart_time=tds[1].get_text().strip()
    tmp = [name, ggstart_time,company, href]
    print(tmp)



