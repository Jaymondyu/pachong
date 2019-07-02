import  urllib.request


# 付费的代理发送
# 1. 用户名与密码(带着)
# 通过验证的处理起来发送

# 第一种付费代理发送请求
def money_proxy_use():
    # 1.代理ip
    money_proxy = {'http':'username:pwd@192.168.12.11:8080'}

    # 2.代理的处理器
    proxy_handler = urllib.request.ProxyHandler(money_proxy)

    # 3.创建的opener
    opener = urllib.request.build_opener(proxy_handler)

    # 4.open发送请求
    response = opener.open('http://www.baidu.com')


#第二种
def money_proxy_use_2():
    # 1.将代理ip的信息写出
    use_name = 'username'
    pwd = 'password'
    proxy_money = '192.168.12.11:8080'

    # 2.创建密码管理器,添加用户名和密码
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    # uri 定位 uri>url
    # url 资源定位符
    password_manager.add_password(None,proxy_money,use_name,pwd)

    # 3.创建可以代理ip的处理器
    handle_auth_proxy = urllib.request.ProxyBasicAuthHandler(password_manager)

    # 4.创建opener
    opener_auth = urllib.request.build_opener(handle_auth_proxy)

    # 5.发动请求
    response = opener_auth.open('http://www.baidu.com')




