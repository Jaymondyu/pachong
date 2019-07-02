import urllib.request

def get_data():

    url = 'http://www.baidu.com'

    # 创建请求对象
    request = urllib.request.Request(url)

    # 请求网络数据
    response = urllib.request.urlopen(request)

    data = response.read().decode()

    # 响应头: response.headers
    # print(response.headers)
    # 获取请求头信息:
    request_header = request.headers

    # 记录获取的信息:
    with open ('header04.html','w',encoding='utf-8') as f:
        f.write(data)




get_data()