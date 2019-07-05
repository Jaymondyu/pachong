#coding:utf-8

import requests
import re
# 下载一个网页
url="http://www.people.com.cn/GB/59476/"


# 模拟浏览器发起http请求
# 使用request库
response = requests.get(url)

# 编码方式
response.encoding = 'GB2312'

#网页源码
html = response.text

name = re.findall(r'<title>(.*?)</title>',html)

#获取信息
td = re.findall(r'<td class="p6">.*?</td>', html,re.S)[0]

#提取标题与对应网址
title_list = re.findall(r'href="(.*?)">(.*?)<',td)

#新建一个文件，用来保存爬到的信息
fb  = open("%s.txt" %name,'w')

# 循环获取新闻信息
for news in title_list:
    news_url,news_title = news

    # 下载新闻内容
    news_response = requests.get(news_url)
    news_response.encoding = 'GB2312'
    news_html = news_response.text

    #提取新闻内容
    news_content = re.findall(r'<p style="text-indent: 2em;">(.*?)</p>',news_html,re.S)
    print(news_content)
