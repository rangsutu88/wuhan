import re

url="<font  style='color:red'>(网)</font>淮北工业与艺术学校地下室墙面维修工程"
# url="淮北工业与艺术学校地下室墙面维修工程<font  style='color:red'>(网)</font>"

# url=re.split(r'(<font.+</font>)',url)
# print(url)
a=url.startswith('<font')
print(a)
