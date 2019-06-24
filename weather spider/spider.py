#coding:utf-8

import requests
import re
from bs4 import BeautifulSoup

url="http://www.tianqihoubao.com/weather/top/jiangjin.html"

response = requests.get(url)

# response.encoding = 'utf-8'

html = response.content.decode('GB2312')

# 提取数据(简单的语法)
# soup会自动整理已有的数据
soup = BeautifulSoup(html,'html.parser')

# td = re.findall(r'<tr>(.*?)<tr>',html,re.S)

tr_list = soup.find_all('tr')

for data in tr_list [1:]:
    sub_data = data.text
    print(sub_data)
