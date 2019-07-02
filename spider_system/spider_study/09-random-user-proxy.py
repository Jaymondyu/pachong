import urllib.request
def proxy_user():
    proxy_list = [
        {"http":"47.107.231.170:8080"},
        {"http": "183.129.207.80:12664"},
        {"http": "60.13.42.99:9999"},
        {"http": "49.70.85.12:9999"},
        {"http": "114.234.80.106:9000"},
        {"http": "175.42.123.35:9999"},
        {"http": "183.129.244.16:12585"},
    ]

    for proxy in proxy_list:

        # print(proxy)
        # 利用遍历出来的ip创建处理器
        proxy_handler = urllib.request.ProxyHandler(proxy)

        # 创建自己的opener
        opener = urllib.request.build_opener(proxy_handler)

        # try:
            # opener.open('https://www.baidu.com',timeout=1)
            # print("haha")
        # except Exception as e:
            # print(e)


proxy_user()