#encoding:utf-8
import re
import sys
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_cookies():
	'''
	获取管理员登陆信息的cookie
	'''

    #  data中内容 是 Data Form中的内容
	url = "http://www.tylinbim.com/login/VerifyLogin.jsp"
	data = {
        "loginfile": "/wui/theme/ecology8/page/login.jsp?templateId=5&logintype=1&gopage=",
        "logintype": "1",
        "fontName": "微软雅黑",
        "message": "",
        "gopage": "",
        "formmethod": "post",
        "rnd": "",
        "serial": "",
        "username": "",
        "isie": "false",
        "islanguid": "7",
        "loginid": "ltyzy",
        "userpassword": "lty1234",
        "submit": "立即登录",
	}
	r = requests.post(url, data=data)

	cookies = dict(r.cookies)
	return cookies

def find_Doc(url):
    cookies = get_cookies()
    # for k,v in cookies.items():
    #     print(k,v)

        # get内容时 要把cookie带上
    response = requests.get(url, cookies=cookies)

    html = response.content#.decode('utf-8')

    print(html)

find_Doc('http://www.tylinbim.com/weaver/weaver.common.util.taglib.SplitPageXmlServlet?tableInstanceId=&tableString=A10DD11BF5E66C0075F87F40208E1C22&pageIndex=0&orderBy=null&otype=null&mode=run&customParams=null&selectedstrs=&pageId=Doc:list')
