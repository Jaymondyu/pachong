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


#############################################################################################################################################################
####################################################悦来晴雨表###############################################################################################
#############################################################################################################################################################

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
        "data":[[today,high_7d[0],weather_7d[0],low_7d[0]],[after_1_day,high_7d[1],weather_7d[1],low_7d[1]],[after_2_day,high_7d[2],weather_7d[2],low_7d[2]],[after_3_day,high_7d[3],weather_7d[3],low_7d[3]],[after_4_day,high_7d[4],weather_7d[4],low_7d[4]],[after_5_day,high_7d[5],weather_7d[5],low_7d[5]],[after_6_day,high_7d[6],weather_7d[6],low_7d[6]]]
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
    judgment = 0
    date = data["date"]
    weather = data["weather"]
    hightemp = data["hightemp"]
    state = data["state"]
    reason = data["reason"]

    if data["weather"].find("雨")!=-1:
        judgment = 1
    if data["hightemp"] >= 35:
        judgment = 2
    if data["weather"].find("雨")!=-1 and data["hightemp"] >= 35:
        judgment = 3


    # 判断是否有重复数据
    sql_try = "select * from yuelai_ where date = "+ "'"+date+"'"
    cursor.execute(sql_try)
    result_try = cursor.fetchall()

    if result_try == []:
        sql_insert = """
                        insert into yuelai_ (date,weather,high_temp,state,reason,judgment) values (%s,%s,%d,%d,%d,%d)
                    """%("'"+date+"'","'"+weather+"'",hightemp,state,reason,judgment)
        cursor.execute(sql_insert)
        conn.commit()
        alart = "已录入新数据"
    else:
        sql_update ="""
                        update yuelai_ set weather = (%s),state=(%d),reason=(%d),judgment=(%d) where date = (%s)
        """%("'"+weather+"'",state,reason,judgment,"'"+date+"'")
        cursor.execute(sql_update)
        conn.commit()
        alart = "已修改数据"

    return alart

# 展示
@app.route("/yuelai/show",methods=["POST"])
def yuelai_show():
    data = request.get_json()
    date = data["date"]
    sql_search = "SELECT date,weather,high_temp,state,reason,judgment from yuelai_ where DATE_FORMAT(date,'%Y-%m')="+'"'+date+'"'+" order by date"
    cursor.execute(sql_search)
    info = cursor.fetchall()
    list = []
    for i in info:
        date = i[0].strftime('%Y-%m-%d')
        weather = i[1]
        hightemp = i[2]
        state = i[3]
        reason = i[4]
        judgment = i[5]

        dict = {
            "date":date,
            "weather":weather,
            "hightemp":hightemp,
            "state":state,
            "reason":reason,
            "judgment":judgment
        }

        list.append(dict)

    return json.dumps(list)

#统计
@app.route("/yuelai/count",methods=["POST"])
def yuelai_count():
    data = request.get_json()
    date = data["date"]
    sql_search = "SELECT date,weather,high_temp,state,reason from yuelai_ where DATE_FORMAT(date,'%Y-%m')="+'"'+date+'"'+" order by date"
    cursor.execute(sql_search)
    info = cursor.fetchall()
    list = []
    rain = 0
    high = 0
    stop = 0
    error =0
    for i in info:
        date = i[0].strftime('%Y-%m-%d')
        weather = i[1]
        hightemp = i[2]
        state = i[3]
        reason = i[4]

        dict = {
            "date":date,
            "weather":weather,
            "hightemp":int(hightemp),
            "state":int(state),
            "reason":int(reason)
        }

        list.append(dict)

    for j in list:
        if j["weather"].find("雨")!=-1:
            rain=rain+1
        if j["hightemp"] >= 35:
            high = high+1
        if j["state"]== 2:
            stop = stop+1
        if j["state"]== 1:
            error = error+1
    dict = {
        "data":{"rain":rain,"hightemp":high,"stop":stop,"error":error}
    }

    return json.dumps(dict)

# 页面
@app.route("/yuelai")
def yuelai_page():
    return render_template("yuelai.html")


#############################################################################################################################################################
####################################################江津晴雨表###############################################################################################
#############################################################################################################################################################

# 7天天气预报
@app.route("/jiangjin/7d")
def jiangjin_7d():
    url = "https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E9%87%8D%E5%BA%86&city=%E9%87%8D%E5%BA%86&county=%E6%B1%9F%E6%B4%A5&callback=jQuery111300454957025127154_1571031806969&_=1571031806980"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        "Referer": "https://tianqi.qq.com/index.htm"
    }
    respone = requests.get(url, headers=headers)
    respone = respone.content.replace('jQuery111300454957025127154_1571031806969(','').replace(')','')
    respone = json.loads(respone)
    respone = respone['data']['forecast_24h']

    today = [respone["1"]["time"],respone["1"]["max_degree"],respone["1"]["day_weather"],respone["1"]["min_degree"]]
    d1 = [respone["2"]["time"],respone["2"]["max_degree"],respone["2"]["day_weather"],respone["2"]["min_degree"]]
    d2 = [respone["3"]["time"],respone["3"]["max_degree"],respone["3"]["day_weather"],respone["3"]["min_degree"]]
    d3 = [respone["4"]["time"],respone["4"]["max_degree"],respone["4"]["day_weather"],respone["4"]["min_degree"]]
    d4 = [respone["5"]["time"],respone["5"]["max_degree"],respone["5"]["day_weather"],respone["5"]["min_degree"]]
    d5 = [respone["6"]["time"],respone["6"]["max_degree"],respone["6"]["day_weather"],respone["6"]["min_degree"]]
    d6 = [respone["7"]["time"],respone["7"]["max_degree"],respone["7"]["day_weather"],respone["7"]["min_degree"]]

    dict_7d = {"data":[today,d1,d2,d3,d4,d5,d6]}

    return json.dumps(dict_7d)

# 实时天气信息
@app.route("/jiangjin/now")
def jiangjin_now():
    url = "http://d1.weather.com.cn/sk_2d/101040500.html?_=1571023248676"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        "Referer": "http://www.weather.com.cn/weather1dn/101040500.shtml"
    }
    respone = requests.get(url, headers=headers)
    respone = respone.content.replace("var dataSK = ","")
    respone = json.loads(respone)

    url_1 = "http://d1.weather.com.cn/dingzhi/101040500.html?_=1571023248678"
    respone_1 = requests.get(url_1, headers=headers)
    respone_1 = respone_1.content
    respone_1 = re.findall('var cityDZ101040500 ={"weatherinfo":(.*?)};',respone_1)[0]
    respone_1 = json.loads(respone_1)



    temp = respone["temp"],
    weather = respone["weather"],
    maxtemp = respone_1["temp"],
    wind = respone["WD"] + respone["WS"],
    humity = "相对湿度"+respone["SD"]

    dict ={
        "data":{
            "temp":int(temp[0]),
            "weather":weather[0],
            "maxtemp":int(maxtemp[0].replace("℃","")),
            "wind":wind[0],
            "humity":humity
        }
    }

    return json.dumps(dict)

# 天气预警
@app.route("/jiangjin/alart")
def jiangjin_alart():
    url = "http://183.66.213.82:8888/weatherlist/jiangjin/7d"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    respone = requests.get(url, headers=headers)
    respone = respone.content
    respone = json.loads(respone)

    rain = 0
    high = 0

    for i in respone["data"]:
        if i[2].find("雨")!=-1:
            rain=rain+1
        if int(i[1]) >=35:
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
@app.route("/jiangjin/insert",methods=["POST"])
def jiangjin_insert():
    data = request.get_json()

    date = data["date"]
    weather = data["weather"]
    hightemp = data["hightemp"]

    # 判断是否有重复数据
    sql_try = "select * from jiangjin where date = "+ "'"+date+"'"
    cursor.execute(sql_try)
    result_try = cursor.fetchall()

    if result_try == []:
        sql_insert = """
                        insert into jiangjin (date,weather,high_temp) values (%s,%s,%d)
                    """%("'"+date+"'","'"+weather+"'",hightemp)
        cursor.execute(sql_insert)
        conn.commit()
        alart = "已录入新数据"
    else:
        sql_update ="""
                        update jiangjin set weather = (%s),high_temp=(%d) where date = (%s)
        """%("'"+weather+"'",hightemp,"'"+date+"'")
        cursor.execute(sql_update)
        conn.commit()
        alart = "已修改数据"

    return alart

# 展示
@app.route("/jiangjin/show",methods=["POST"])
def jiangjin_show():
    data = request.get_json()
    date = data["date"]
    sql_search = "SELECT date,weather,high_temp from jiangjin where DATE_FORMAT(date,'%Y-%m')="+'"'+date+'"'+" order by date"
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

# 页面
@app.route("/jiangjin")
def jiangjin_page():
    return render_template("jiangjin.html")


application = app
if __name__ == '__main__':
	app.run(host="0.0.0.0",port=8808, debug=True)