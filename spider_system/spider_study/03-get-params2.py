import urllib.request
import urllib.parse
import string

# 此为get方法
def get_params():
    url = 'http://www.baidu.com/s?'

    parmas = {
        "wd":'中文',
        'key':"zhang",
        "value":"san"
    }

    # parmas中 只有wd用到了 其他都没有用到

    str_parmas = urllib.parse.urlencode(parmas)


    final_url = url + str_parmas


    # 将包含汉字的url进行转译:
    result = urllib.parse.quote(final_url,safe=string.printable)

    # 使用代码发送网络请求
    response = urllib.request.urlopen(result)

    data = response.read().decode("utf-8")

    # 保存到本地
    with open("search03.html", "w", encoding='utf-8')as f:
        f.write(data)



get_params()