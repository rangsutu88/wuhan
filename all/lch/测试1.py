import datetime
import json
import time

import pandas as pd

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree


# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://www.postgres.cn/v2/document"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
#
#
#
# locator = (By.XPATH, '//div[@class="well well-sm"][1]')
#
# WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
# time.sleep(2)
#
# page=driver.page_source
#
# print(page)

page="""
<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" lang="en"><head>
    <meta charset="UTF-8" />
	<title>文档目录/Document Index: 世界上功能最强大的开源数据库...</title>
    <link rel="stylesheet" href="/js/bootstrap-3.3.7-dist/css/bootstrap.min.css" />
    <link rel="stylesheet" href="/css/v2/style.css" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <script src="/js/jquery-3.3.1.min.js"></script>
    <script src="/js/bootstrap-3.3.7-dist/js/bootstrap.min.js"></script>
	<script src="/js/showdown.min.js" type="text/javascript" charset="utf-8"></script>

</head>
<body>
<!--头部-->
<header>
    <!--导航栏-->
    <nav class="navbar bg_blue navbar-fixed-top">
        <div class="container">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
		<a class="navbar-brand" href="https://postgresql.org" target="_blank"><img class="logo" src="/images/elephant_logo.png" width="32" height="32" /></a> 
                <a class="navbar-brand" href="/v2/home">PostgreSQL中文社区</a>
            </div>
            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav">
                    <li><a href="/v2/home">首页 <span class="sr-only">(current)</span></a></li>
                    <li><a href="/v2/news">社区新闻</a></li>
                    <li><a href="/v2/faq">有问有答(FAQ)</a></li>
                    <li><a href="/v2/about">了解PostgreSQL</a></li>
		<!--			<li><a href="/home">V1</a></li> -->

                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">相关资料 <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="/v2/book">图书</a></li>
                            <li><a href="/v2/document">文档资料</a></li>
                            <li><a href="/v2/download">软件下载</a></li>
                            <li><a href="/v2/community">关于中文社区</a></li>
                        </ul>
                    </li>
                </ul>
                <form class="navbar-form navbar-left" name="srch" action="/v2/search" method="post">
                    <div class="form-group">
                        <input type="text" class="form-control" name="keysrh" placeholder="Search" />
                    </div>
                </form>

<ul class="nav navbar-nav navbar-right"><li><a href="/v2/act/register">注册</a></li><li><a href="/v2/act/userinfo">登录</a></li></ul>


            </div><!-- /.navbar-collapse -->
        </div><!-- /.container-fluid -->
    </nav>
    <!--头部图片-->
    <div class="header_img bg_blue">
        <!--可放一张图片-->
        <!--<div class="container pageTitle">
            <h4>世界上功能最强大的开源数据库</h4>
            <h1>PostgreSQL中文社区</h1>
            <h4>www.postgres.cn</h4>
        </div>-->
    </div>
</header>


<!--中间部分-->
<div class="container" style="margin-top: 60px">
    <!--左边导航栏-->
    <div class="col-md-3">
        <div class="well">
            <ul class="nav nav-pills nav-stacked">
                <li><a href="/v2/book">图书</a></li>
                <li class="active"><a href="###">文档资料<span class="badge pull-right">*</span></a></li>
                <li><a href="/v2/download">软件下载</a></li>
                <li><a href="/v2/community">关于中文社区</a></li>
            </ul>
        </div>

    </div>
    <!--右边内容部分-->
    <div class="col-md-9">
        <div class="well">
            <!--分级导航-->
            <ol class="breadcrumb">
                <li><a href="/v2/home">首页</a></li>
                <li><a href="#">相关资料</a></li>
                <li class="active"><a href="#">文档资料</a></li>
            </ol>
            <!--文档列表-->
            <div class="well well-sm" style="position: relative;">
                <h4><a target="_blank" href="/docs/10/">PostgreSQL 10.1 版本在线手册 ...(中文版本)</a></h4>
                <p>感谢瀚高软件的韩悦悦、陈华军等翻译小组的辛苦工作。</p>
                <img src="/image/new_mark.jpg" width="50" style="position: absolute;right: -3px;top: -3px;" /><!--新的内容右角标-->
            </div>
            <div class="well well-sm">
                <h4><a target="_blank" href="/docs/9.6/index.html">PostgreSQL 9.6.0 版本在线手册 ...(中文版本) ... (英文原版)</a></h4>
            </div>
            <div class="well well-sm">
                <h4><a target="_blank" href="/docs/9.5/index.html">PostgreSQL 9.5.3 版本在线手册 ... (中文版本) ... (英文原版)</a></h4>
            </div>
            <div class="well well-sm">
                <h4><a target="_blank" href="/docs/9.4/index.html">PostgreSQL 9.4.4 版本在线手册 ... (中文版本) ... (英文原版)</a></h4>
            </div>
            <div class="well well-sm">
                <h4><a href="/news/typelist/1/会议资料">PostgreSQL 历年大会资料汇总</a></h4>
            </div>
            <div class="well well-sm">
                <h4><a target="_blank" href="https://postgres-cn.github.io/pgbouncer-doc/">pgbouncer 1.7.2版本在线手册 ...(中文版本)</a></h4>
            </div>
            <div class="well well-sm">
                <h4><a target="_blank" href="https://gp-docs-cn.github.io/docs/">Greenplum 数据库中文文档</a></h4>
                <p>感谢武汉大学 彭煜玮，邰凌翔，韩珂，兰海 翻译。 感谢 VitesseData/迅讯科技 提供支持。</p>
            </div>
            <div class="well well-sm">
                <h4><a target="_blank" href="/v2/document/faq"> 一般常见问题汇总(FAQ)</a></h4>
            </div>
            <div class="well well-sm">
                <h4><a target="_blank" href="/v2/document/dev_faq">开发人员常见问题汇总(DEV_FAQ)</a></h4>
            </div>
            <div class="well well-sm">
                <h4><a target="_blank" href="/v2/document/win_faq">Windows平台安装PostgreSQL常见问题及解答</a></h4>
            </div>

        </div>

    </div>
</div>





<!--底部-->
<footer class="bottom bg_blue">
    <div class="container" style="padding: 20px">
        <div class="col-md-1"></div>
        <div class="col-md-3">
            <p><strong>加入我们：</strong></p>
            <ul class="QQnum">
                <li>QQ群1：5276420</li>
                <li>QQ群2：3336901</li>
                <li>QQ群3：254622631</li>
                <li>文档群：150657323</li>
            </ul>
        </div>
        <div class="col-md-3 support">
            <p><a href="#"><strong>商业支持：</strong></a></p>
            <ul class="QQnum">
                <li><a target="_blank" href="http://w3.ww-it.cn/">成都文武信息技术有限公司</a></li>
                <li><a target="_blank" href="http://www.cstech.ltd/">杭州乘数科技有限公司</a></li>
                <li><a target="_blank" href="https://www.aliyun.com/product/rds/postgresql?spm=5176.198144.cloudEssentials.44.b68d346dRG9UL4">阿里云</a></li>
                <li><a target="_blank" href=" https://www.qingcloud.com/products/postgresql/">青云(北京优帆科技有限公司)</a></li>
            </ul>
        </div>
        <div class="col-md-3 ">
            <p><a href="#" style="color: #333;"><strong>扫码关注：</strong></a></p>
            <div class="wechat_jpg">
                <img src="/image/wechat.jpg" alt="扫描关注微信" />
                <a target="_blank" href="http://weibo.com/postgresqlchina"><img src="/image/weibo.jpg" alt="扫描关注微博" /></a>
            </div>

        </div>
    </div>
</footer>


<div id="pgFooter" style="font-size:10px;font-family:arial">
           © 2010 PostgreSQL中文社区
           <script type="text/javascript">var cnzz_protocol = (("https:" == document.location.protocol) ? " https://" : " http://");document.write(unescape("%3Cspan id='cnzz_stat_icon_1256993191'%3E%3C/span%3E%3Cscript src='" + cnzz_protocol + "s4.cnzz.com/z_stat.php%3Fid%3D1256993191%26show%3Dpic' type='text/javascript'%3E%3C/script%3E"));</script><span id="cnzz_stat_icon_1256993191"><a href="https://www.cnzz.com/stat/website.php?web_id=1256993191" target="_blank" title="站长统计"><img border="0" hspace="0" vspace="0" src="http://icon.cnzz.com/img/pic.gif" /></a></span><script src=" http://s4.cnzz.com/z_stat.php?id=1256993191&amp;show=pic" type="text/javascript"></script><script src="http://c.cnzz.com/core.php?web_id=1256993191&amp;show=pic&amp;t=z" charset="utf-8" type="text/javascript"></script>



</div></body></html>
"""

content=etree.HTML(page)
node=content.xpath('//div[@class="well well-sm"][1]//text()')
print(len(node))
for i in node:
    print(i)