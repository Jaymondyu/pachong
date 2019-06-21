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

#获取信息
td = re.findall(r'<td class="p6">.*?</td>', html,re.S)

print(td)

