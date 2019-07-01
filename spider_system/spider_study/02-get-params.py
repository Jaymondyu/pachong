import urllib.request
import urllib.parse
import string

def get_method_params():

    url = 'http://www.baidu.com/s?wd='
    # 拼接字符串(汉字)
    # 将关键字拼接在url中,达到可随时更换关键字的目的

    keyword = "美女"

    final_url = url + keyword
    # url中的汉字,需要转译才能使用,因为ASCII中是没有汉字的

    # 将包含汉字的url进行转译:
    new_url = urllib.parse.quote(final_url,safe = string.printable)



    # 使用代码发送网络请求
    response = urllib.request.urlopen(new_url)

    data = response.read().decode("utf-8")



    # 保存到本地
    with open("search02.html","w",encoding='utf-8')as f:
        f.write(data)





get_method_params()