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

conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='weather_database',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()

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
    weather = re.findall(r'<div class="weather dis">(.*?)</div>',respone)[0]
    maxtemp = re.findall(r'<div id="maxTempDiv"><img src="http://i.tq121.com.cn/i/weather2017/max.png"><span>(.*?)</span></div>',respone)[0].replace("℃","")
    wind = re.findall(r'<p><img src="http://i.tq121.com.cn/i/weather2017/windIcon.png"><span>(.*?)</span></p>',respone)[0]
    humity = re.findall(r'<p><img src="http://i.tq121.com.cn/i/weather2017/sdIcon.png"><span>(.*?)</span></p>',respone)[0]

    dict ={
        "data":{
            "temp":int(temp),
            "weather":weather,
            "maxtemp":int(maxtemp),
            "wind":wind,
            "humity":humity
        }
    }

    return json.dumps(dict)

# 天气预警
@app.route("/yuelai/alart")
def yuelai_alart():
    url = "http://forecast.weather.com.cn/town/weathern/101040700026.shtml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    respone = requests.get(url, headers=headers)
    respone = respone.content

    data_high = re.findall(r'var eventDay =(.*?);', respone)[0].replace("[", "").replace("]", "").replace('"', "")

    high_7d = data_high.split(',')[1:]
    weather_7d = re.findall(r'<p class="weather-info" title="(.*?)">', respone, re.S)

    rain = 0
    for i in weather_7d:
        if i.find("雨")!=-1:
            rain=rain+1
    high = 0
    for l in high_7d:
        if int(l) >=35:
            high = high +1

    dict = {
        "data":{
            "rain":rain,
            "high":high,
            "wind":0,
            "typhoon":0
        }
    }

    return json.dumps(dict)

# 录入
@app.route("/yuelai/insert",methods=["POST"])
def yuelai_insert():
    data = request.get_json()

    date = data["date"]
    weather = data["weather"]
    hightemp = data["hightemp"]

    # 判断是否有重复数据
    sql_try = "select * from yuelai where date = "+ "'"+date+"'"
    cursor.execute(sql_try)
    result_try = cursor.fetchall()

    if result_try == []:
        sql_insert = """
                        insert into yuelai (date,weather,high_temp) values (%s,%s,%d)
                    """%("'"+date+"'","'"+weather+"'",hightemp)
        cursor.execute(sql_insert)
        conn.commit()
        alart = "已录入新数据"
    else:
        sql_update ="""
                        update yuelai set weather = (%s) where date = (%s)
        """%("'"+weather+"'","'"+date+"'")
        cursor.execute(sql_update)
        conn.commit()
        alart = "已修改数据"

    return alart

# 展示
@app.route("/yuelai/show",methods=["POST"])
def yuelai_show():
    data = request.get_json()
    date = data["date"]
    sql_search = "SELECT date,weather,high_temp from yuelai where DATE_FORMAT(date,'%Y-%m')="+'"'+date+'"'+" order by date"
    cursor.execute(sql_search)
    info = cursor.fetchall()
    list = []
    for i in info:
        date = i[0].strftime('%Y-%m-%d')
        weather = i[1]
        hightemp = i[2]

        dict = {
            "date":date,
            "weather":weather,
            "hightemp":hightemp
        }

        list.append(dict)

    return json.dumps(list)



application = app
if __name__ == '__main__':
	app.run(host="0.0.0.0",port=8888, debug=True)