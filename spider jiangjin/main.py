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
	url = "https://www.mikecrm.com/contact.php"
	data = {
		"d": '{"cvs":{"al":1,"a":"zf2211@163.com","p1":"098795f5e186dd0aa122b3c945045069","p2":"0987b59cfce7a2725dae8a855b03a90c"}}'
	}
	r = requests.post(url, data=data)

	cookies = dict(r.cookies)
	return cookies

def find_Doc(url):
    cookies = get_cookies()
    # for k,v in cookies.items():
    #     print(k,v)

        # get内容时 要把cookie带上
    data={"d":'{"cvs":{"i":200412098}}'}
    response = requests.get(url, cookies=cookies,data=data)

    html = response.content#.decode('utf-8')

    print(html)

find_Doc('https://www.mikecrm.com/handler/web/form_submit/handleGetListFormSubmitSummary.php')
