import re
url='http://www.laztb.gov.cn/laztb/jyxx/002001/002001001/002001001001/'

mark=url.strip('/').rsplit('/',maxsplit=1)[1]
print(mark)