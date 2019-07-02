import urllib.request

def get_data():

    url = 'https://www.baidu.com'

    # 添加请求头的信息
    # header = {
    #     # 浏览器的版本
    #     "User-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    # }





    # 创建请求对象(header放在此处)
    # request = urllib.request.Request(url,headers=header)   #使用上面的表单设施header时 使用这个
    request = urllib.request.Request(url)

    # 动态的去添加header的信息
    header = request.add_header("User-agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36")




    # 请求网络数据 (不在此处增加请求头信息,因为此方法没有提供参数)
    response = urllib.request.urlopen(request)

    data = response.read().decode()

    # 响应头: response.headers
    # print(response.headers)

    # 获取请求头信息(打印所有的请求头信息):
    request_headers = request.headers
    # print(request_headers)

    # 打印特定的请求头信息
    # 注意只有首字母需要大写,其他字母都小写
    request_User_agent = request.get_header('User-agent')
    print(request_User_agent)


    # 记录获取的信息:
    with open ('header04.html','w',encoding='utf-8') as f:
        f.write(data)




get_data()