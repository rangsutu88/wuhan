html='''

<html><head><title >The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a class="sister" href="http://example.com/elsie" id="link1"><!--Elsie--></a>,
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
and they lived at the bottom of a well.</p>
<p class="story">...</p>

'''

from bs4 import BeautifulSoup
soup=BeautifulSoup(html,'lxml')
title=soup.find_all('a')
for i in title:
    title1=i.string
    title2=i.get_text()
    print(title1)

    print(title2)