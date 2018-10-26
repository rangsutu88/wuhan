import re
#
# url='http://www.zsggzy.com/news_,11,12,22,_%D5%FE%B8%AE%B2%C9%B9%BA_1___.html'
#
# mark=re.findall('news_,(.+),_',url)[0]
# print(mark)
import time

url='http://www.fzztb.gov.cn/jsgc/zbgs/yqzb/index_1.htm'
mark=re.findall('/((\w+?)/(\w+?))/index',url)[0][0]

print(mark)

print(5//2)