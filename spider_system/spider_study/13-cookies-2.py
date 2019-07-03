import urllib.request
from http import cookiejar
from urllib import parse

def spider():
# 1.代码登录
    # 1.1 登陆的网址
    login_url = 'http://www.tylinbim.com/login/VerifyLogin.jsp'

    # 1.2 登录的参数
    login_form_data = {
        'loginfile': '/wui/theme/ecology8/page/login.jsp?templateId=5&logintype=1&gopage=',
        'logintype': '1',
        'fontName': '微软雅黑',
        'message':'',
        'gopage':'',
        'formmethod': 'post',
        'rnd':'',
        'serial':'',
        'username':'',
        'isie': 'false',
        'islanguid': '7',
        'loginid': 'ltyzy',
        'userpassword': 'lty1234',
        'submit': '立即登录'
    }

    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }

    #发送post登录请求

    # 定义保存cookie的cookiejar
    cookie_jar = cookiejar.CookieJar()

    # 定义有添加cookie功能的处理器
    cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)

    # 生成opener
    opener = urllib.request.build_opener(cookie_handler)

    # 转译     1.参数需要转译   2.post请求的data要求是bytes
    str_data = urllib.parse.urlencode(login_form_data).encode('utf-8')

    # 带着参数发送post请求
    login_request = urllib.request.Request(login_url,headers=headers,data=str_data)

    # 如果登陆成功,cookiejar自动保存cookie
    opener.open(login_request)

# 2.代码带着cookie去访问目标url
    target_url = 'http://www.tylinbim.com/weaver/weaver.common.util.taglib.SplitPageXmlServlet?tableInstanceId=&tableString=9FD12026ABC602B815CA09F52BB7E4F3&pageIndex=0&orderBy=null&otype=null&mode=run&customParams=null&selectedstrs=&pageId=Doc:list'

    target_request = urllib.request.Request(target_url,headers=headers)

    respose = opener.open(target_url)

    data = respose.read().decode('GBK')

    with open('13cookies.html','w',encoding='GBK') as f:
        f.write(data)




spider()