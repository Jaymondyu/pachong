#coding:utf-8
import requests
import re
import json
import flask

app = flask.Flask(__name__)

@app.route("/")
def weather_hours():

    day = []

    url = 'http://www.weather.com.cn/weather1d/101290101.shtml'

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    }

    # request = urllib.request.Request(url,headers=headers)

    response = requests.get(url)

    data = response.text

    data_weather = re.findall(r"\"7d\":\[(.*?)]}",data,re.S)


    # print(json.loads("["+data_weather[0]+"]")[0])

    for i in json.loads("["+data_weather[0]+"]"):
        for l in i:
            arr = l.split(',')
            day.append([arr[0],arr[2],arr[3]])

    hours = day[:8]


    return json.dumps(hours)

@app.route("/7d")
def weather_qq():

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E5%B9%BF%E4%B8%9C&city=%E6%B7%B1%E5%9C%B3&county=&callback=jQuery111307645707250197813_1564455732836&_=1564455732841'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    hello = data["data"]["forecast_24h"]

    rainNum = 0
    tfNum = 0
    High = 0
    Low = 0
    for m in range(1, 8):
        if (str(hello[str(m)]).find("雨") != -1):
            rainNum += 1
        if (str(hello[str(m)]).find("台风") != -1):
            tfNum += 1
        if int(hello[str(m)]["max_degree"]) > 35:
            High += 1
        if int(hello[str(m)]["min_degree"]) < 5:
            Low += 1

    Tea = [rainNum, tfNum, High, Low]

    final = [hello, Tea]


    return json.dumps(final)


application = app
if __name__ == '__main__':
	app.run(host="0.0.0.0",port=8808, debug=True)