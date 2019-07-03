"""

直接获取 个人中心的页面
手动粘贴 复制PC抓报的cookies
放在 requests 对象的请求头里面


"""


import  urllib.request

url = 'https://account.bilibili.com/account/home'

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    # "Cookie":"_uuid=876F1B37-CF31-F9E2-F1D9-03AB07E556C474756infoc; buvid3=18B2CA6F-1011-4529-9BED-0651005EE13482017infoc; LIVE_BUVID=AUTO6115483201882192; sid=hw1oxv8q; stardustvideo=1; CURRENT_FNVAL=16; rpdid=|(umukk~JJ~)0J'ull~~mkl)J; im_notify_type_13317995=0; UM_distinctid=16ab9f40395510-0eebfd8b4c4c8b-3e385e0c-1fa400-16ab9f40396272; CURRENT_QUALITY=80; fts=1558336300; DedeUserID=13317995; DedeUserID__ckMd5=d8aa89b2c433e932; finger=b3372c5f; SESSDATA=bfedf551%2C1563346078%2C114a1461; bili_jct=27841422307d3b9a506b36d1cfe1484c; bp_t_offset_13317995=271742477742849826"
}

request = urllib.request.Request(url,headers=headers)

response = urllib.request.urlopen(url)

data = response.read().decode("utf-8")

with open('12cookies.html','w',encoding='utf-8') as f:
    f.write(data)