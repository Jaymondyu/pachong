#coding:utf-8
from flask import Flask,request,render_template
import requests
import mysql.connector
import datetime
import os
import re
import json
from dateutil.relativedelta import relativedelta
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

# 7天天气预报
@app.route("/yuelai/7d")
def yuelai_7d():
    url = "http://forecast.weather.com.cn/town/weathern/101040700026.shtml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    respone = requests.get(url, headers=headers)
    respone = respone.content
    data_high = re.findall(r'var eventDay =(.*?);', respone)[0].replace("[", "").replace("]", "").replace('"', "")
    data_low = re.findall(r'var eventNight = (.*?);', respone)[0].replace("[", "").replace("]", "").replace('"', "")

    high_7d = data_high.split(',')[1:]
    low_7d = data_low.split(',')[1:]

    datetime_now = datetime.datetime.now()
    today = datetime_now.strftime("%Y-%m-%d")
    after_1_day = (datetime_now + relativedelta(days=1)).strftime("%Y-%m-%d")
    after_2_day = (datetime_now + relativedelta(days=2)).strftime("%Y-%m-%d")
    after_3_day = (datetime_now + relativedelta(days=3)).strftime("%Y-%m-%d")
    after_4_day = (datetime_now + relativedelta(days=4)).strftime("%Y-%m-%d")
    after_5_day = (datetime_now + relativedelta(days=5)).strftime("%Y-%m-%d")
    after_6_day = (datetime_now + relativedelta(days=6)).strftime("%Y-%m-%d")

    weather_7d = re.findall(r'<p class="weather-info" title="(.*?)">', respone, re.S)

    dict_7d = {
        "data": {
            "x": [today, after_1_day, after_2_day, after_3_day, after_4_day, after_5_day, after_6_day],
            "high": high_7d,
            "low": low_7d,
            "weather": weather_7d
        }
    }

    return json.dumps(dict_7d)

# 实时天气信息
@app.route("/yuelai/now")
def yuelai_now():
    url = "http://forecast.weather.com.cn/town/weather1dn/101040700026.shtml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    respone = requests.get(url, headers=headers)
    respone = respone.content

    temp = re.findall(r'<span class="temp">(.*?)</span>',respone)[0]

    return temp














application = app
if __name__ == '__main__':
	app.run(host="0.0.0.0",port=8888, debug=True)