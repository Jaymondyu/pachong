import urllib.request

def create_proxy_handler():

    url = "https://blog.csdn.net/weixin_42144379/article/details/85639397"

    # 添加代理
    proxy = {
        # 免费写法
        "http":"http://47.107.231.170:8080"
        # 免费写法2
        # "http":"47.107.231.170:8080"

        #付费代理写法
        # "http":"用户名":密码@ip地址



    }

    # 代理处理器
    proxy_handler = urllib.request.ProxyHandler(proxy)

    # 创建自己的opener
    opener = urllib.request.build_opener(proxy_handler)

    # 拿着代理ip去发送请求
    data = opener.open(url).read()
    print(data)

create_proxy_handler()