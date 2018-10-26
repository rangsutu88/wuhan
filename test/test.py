# import requests
# from selenium import webdriver
# import json
# driver=webdriver.Chrome()
# driver.get('http://ggzyjy.ntzw.gov.cn/jyxx/tradeInfo.html')
#
# cookie = driver.get_cookies()
# driver.quit()
#
# cookies = {}
# for i in cookie:
#     cookies['{}'.format(i['name'])] = i['value']
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
#                   '(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
#
# }
#
# req = requests.get(url='http://ggzyjy.ntzw.gov.cn/services/XzsJsggWebservice/'
#                        'getList?response=application/json&pageIndex={page}&'
#                        'pageSize=15&&categorynum=003004007&diqu2=&xmlx=&xmmc='.format(page=2),
#                    headers=headers, cookies=cookies, timeout=4)
# data=[]
# con=req.json()
# ret=con['return']
# ret=json.loads(ret)
#
# tables=ret['Table']
# for table in tables:
#     href=table['href']
#     title=table['title']
#     jyfl=table['jyfl']
#     city=table['city']
#     jyfs=table['jyfs']
#     postdate=table['postdate']
#     tmp=[href,title,jyfl,city,jyfs,postdate]
#     data.append(tmp)
# print(data)
#     # print(req.json())
import re

st='ni/345/12/hh'
s='ccccccccccc'
req=st.rsplit('/')[0]
print(req)