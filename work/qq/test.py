for i in range(10):
    url='1 {}'.format(i) +'\n'
    print('出错了{}'.format(url))
    with open('未爬取到的链接.txt','a+',encoding='utf8') as f:
        f.write(url)