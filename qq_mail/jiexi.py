from bs4 import BeautifulSoup
import time
import re
soup=BeautifulSoup(open('soup.html',encoding='GB18030'),'lxml')
# print(soup.title)
conent=soup.find('div',class_='readmailinfo')
# print(conent)
tables=conent.find_all('table',limit=3)
title=tables[0].find('span').get_text()
send_bys=tables[1].find_all('span')
send_by=send_bys[1].get_text()
lasts=tables[2].find_all('tr',limit=2)
send_time=lasts[0].b.get_text()
send_to=lasts[1].get_text()
send_to=send_to.lstrip('收件人：').strip()
send_by_email=re.findall(r'<(.+)>',send_by)[0]

print(title)
print(send_by)
print(send_time)
print(send_to)
print(send_by_email)
