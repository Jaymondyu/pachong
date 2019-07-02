import urllib.request

def handler_openner():
    # 系统的 urlopen() 并没有添加代理的功能,所以需要我们自定义这个功能
    # 安全套阶层: ssl第三方的CA数字证书
    # http 使用的80端口, https使用的443端口
    # urlopen()为什么可以请求数据? ------->  handler处理器
    # 自己的openner请求数据


    # urllib.request.urlopen()
    url = "https://blog.csdn.net/weixin_42144379/article/details/85639397"

    # 创建自己的处理器
    handler = urllib.request.HTTPHandler()

    # 创建自己的openner
    urllib.request.build_opener()
