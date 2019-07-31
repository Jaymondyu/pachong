#coding:utf-8
import requests
import re
import json
import flask

app = flask.Flask(__name__)

@app.route("/shenzhen")
def shenzhen_hours():


    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E5%B9%BF%E4%B8%9C&city=%E6%B7%B1%E5%9C%B3&county=&callback=jQuery1113035920872837971163_1564533727240&_=1564533727245'

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])

    world = data["data"]["forecast_1h"]



    return json.dumps(world)



@app.route("/shenzhen/7d")
def shenzhen_7d():

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E5%B9%BF%E4%B8%9C&city=%E6%B7%B1%E5%9C%B3&county=&callback=jQuery111307645707250197813_1564455732836&_=1564455732841'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    hello = data["data"]["forecast_24h"]

    # rainNum = 0
    # tfNum = 0
    # High = 0
    # Low = 0
    # for m in range(1, 8):
    #     if (str(hello[str(m)]).find("雨") != -1):
    #         rainNum += 1
    #     if (str(hello[str(m)]).find("台风") != -1):
    #         tfNum += 1
    #     if int(hello[str(m)]["max_degree"]) > 35:
    #         High += 1
    #     if int(hello[str(m)]["min_degree"]) < 5:
    #         Low += 1
    #
    # Tea = [rainNum, tfNum, High, Low]



    return json.dumps(hello)



@app.route("/shenzhen/alarm")
def shenzhen_alarm():

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E5%B9%BF%E4%B8%9C&city=%E6%B7%B1%E5%9C%B3&county=&callback=jQuery1113035920872837971163_1564533727240&_=1564533727245'

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])

    warning = data["data"]["alarm"]



    url_1 = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E5%B9%BF%E4%B8%9C&city=%E6%B7%B1%E5%9C%B3&county=&callback=jQuery111307645707250197813_1564455732836&_=1564455732841'



    response_1 = requests.get(url_1)

    data_1 = response_1.text

    data_1 = json.loads(data_1[data_1.find('{'):-1])


    hello_1 = data["data"]["forecast_24h"]

    High = 0
    Rain = 0

    for m in range(1, 8):
        if int(hello_1[str(m)]["max_degree"]) > 35:
            High += 1
        if (str(hello_1[str(m)]).find("\u96e8") != -1):
            Rain += 1


    if (str(warning).find("\u53f0\u98ce") != -1):
        tf = 1
    else:
        tf = 0


    if (str(warning).find("\u96f7\u7535") != -1):
        ld = 1
    else:
        ld = 0

    alarm=[tf,ld,Rain,High]

    return json.dumps(alarm)




application = app
if __name__ == '__main__':
	app.run(host="0.0.0.0",port=8808, debug=True)