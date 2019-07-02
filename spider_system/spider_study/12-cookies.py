"""

直接获取 个人中心的页面
手动粘贴 复制PC抓报的cookies

"""



import  urllib.request

url = 'http://www.tylinbim.com/wui/main.jsp'

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
}

request = urllib.request.Request(url,headers=headers)

response = urllib.request.urlopen(url)

data = response.read().decode("utf-8")

with open('12cookies.html','w',encoding='utf-8') as f:
    f.write(data)