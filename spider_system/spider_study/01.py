import urllib.request

# 将百度首页直接爬下来了

def get_data():
    url = 'http://www.baidu.com/'

    # 打开相应网址
    response = urllib.request.urlopen(url)

    # 读取网页内容(bytes类型)
    data = response.read()

    # 将内容转换成字符串
    str_data = data.decode("utf-8")

    # 将数据写入文件
    with open("baidu01.html","w",encoding='utf-8')as f:
        f.write(str_data)

    # 将字符串类型转换成bytes
    # str_name = 'baidu'
    # bytes_name = str_name.encode("utf-8")
    # print(bytes_name)

    #python爬取的类型: bytes或str
    # 如果爬取回来的是bytes类型,但是你写入的时候需要str decode('utf-8')
    # 如果爬取回来的是str类型,但是你写入的时候需要bytes decode('utf-8')


get_data()