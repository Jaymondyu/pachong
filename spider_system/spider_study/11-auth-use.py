# 爬取自己公司的数据做数据分析

import urllib.request


def auth_nei_wang():

    # 1.用户名密码
    user = 'admin'
    pwd = 'admin123'
    nei_url = 'http://192.168.179.66'


    # 2.创建密码管理器
    pwd_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()

    pwd_manager.add_password(None,nei_url,user,pwd)

    # 3.创建认证处理器
    auth_handler = urllib.request.HTTPBasicAuthHandler(pwd_manager)

    # 4.创建opener
    opener = urllib.request.build_opener(auth_handler)

    # 5.发送请求
    response = opener.open(nei_url)


