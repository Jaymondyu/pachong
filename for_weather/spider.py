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

    list = [world['0'],world['1'],world['2'],world['3'],world['4'],world['5'],world['6'],world['7'],world['8'],world['9'],world['10'],world['11']]

    return json.dumps(list)

@app.route("/shenzhen/now")
def shenzhen_now():


    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E5%B9%BF%E4%B8%9C&city=%E6%B7%B1%E5%9C%B3&county=&callback=jQuery1113035920872837971163_1564533727240&_=1564533727245'

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])

    world = data["data"]["observe"]

    list = [world]

    return json.dumps(list)

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

    list = [hello['1'],hello['2'],hello['3'],hello['4'],hello['5'],hello['6'],hello['7']]





    return json.dumps(list)

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

@app.route("/guandu/7d_0")
def hospital0():

    list=[]

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E4%BA%91%E5%8D%97&city=%E6%98%86%E6%98%8E&county=%E5%AE%98%E6%B8%A1&callback=jQuery1113015777097108962002_1564621494015&_=1564621494020'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    list.append(rua['0'])

    return json.dumps(list)

@app.route("/guandu/7d_1")
def hospital1():

    list=[]

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E4%BA%91%E5%8D%97&city=%E6%98%86%E6%98%8E&county=%E5%AE%98%E6%B8%A1&callback=jQuery1113015777097108962002_1564621494015&_=1564621494020'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    list.append(rua['1'])

    return json.dumps(list)

@app.route("/guandu/7d_2")
def hospital2():

    list=[]

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E4%BA%91%E5%8D%97&city=%E6%98%86%E6%98%8E&county=%E5%AE%98%E6%B8%A1&callback=jQuery1113015777097108962002_1564621494015&_=1564621494020'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    list.append(rua['2'])

    return json.dumps(list)

@app.route("/guandu/7d_3")
def hospital3():

    list=[]

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E4%BA%91%E5%8D%97&city=%E6%98%86%E6%98%8E&county=%E5%AE%98%E6%B8%A1&callback=jQuery1113015777097108962002_1564621494015&_=1564621494020'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    list.append(rua['3'])

    return json.dumps(list)

@app.route("/guandu/7d_4")
def hospital4():

    list=[]

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E4%BA%91%E5%8D%97&city=%E6%98%86%E6%98%8E&county=%E5%AE%98%E6%B8%A1&callback=jQuery1113015777097108962002_1564621494015&_=1564621494020'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    list.append(rua['4'])

    return json.dumps(list)

@app.route("/guandu/7d_5")
def hospital5():

    list=[]

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E4%BA%91%E5%8D%97&city=%E6%98%86%E6%98%8E&county=%E5%AE%98%E6%B8%A1&callback=jQuery1113015777097108962002_1564621494015&_=1564621494020'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    list.append(rua['5'])

    return json.dumps(list)

@app.route("/guandu/7d_6")
def hospital6():

    list=[]

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E4%BA%91%E5%8D%97&city=%E6%98%86%E6%98%8E&county=%E5%AE%98%E6%B8%A1&callback=jQuery1113015777097108962002_1564621494015&_=1564621494020'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    list.append(rua['6'])

    return json.dumps(list)

@app.route("/guandu/7d_7")
def hospital7():

    list=[]

    url = 'https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E4%BA%91%E5%8D%97&city=%E6%98%86%E6%98%8E&county=%E5%AE%98%E6%B8%A1&callback=jQuery1113015777097108962002_1564621494015&_=1564621494020'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    rainNum = 0

    High = 0

    for m in range(2, 7):
        if (str(rua[str(m)]).find("\u96e8") != -1):
            rainNum += 1

    if int(rua[str(1)]["max_degree"]) > 35:
        High += 1

    dic = {}
    if rainNum >0:
        dic["rain"] = "未来可能有雨，注意安全施工"
        # rain = {"rain":"未来可能有雨，注意安全施工"}
    else:
        dic["rain"] = "未来几天无雨"
        # rain = {"rain": "未来几天无雨"}

    if High > 0:
        dic["high"] = "高温天气，注意防暑"
        # High = {"high":"高温天气，注意防暑"}
    else:
        # High = {"high": "无高温预警"}
        dic["high"] = "无高温预警"
    list = [dic]
    return json.dumps(list)

@app.route("/guandu/select")
def select():
    id = flask.request.args.get("id")
    if id == "1":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/s.action?url=EzY73m'
    elif id == "2":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/s.action?url=rMv2Az'

    elif id == "3":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/s.action?url=AjEN7f'

    elif id == "4":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/s.action?url=jAvyYb'

    else:
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/s.action?url=vYJRfm'

@app.route("/jiangjin/7d_1")
def jiangjin1():

    list=[]

    url = "https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E9%87%8D%E5%BA%86&city=%E9%87%8D%E5%BA%86&county=%E6%B1%9F%E6%B4%A5&callback=jQuery111307596638576679418_1564706624996&_=1564706625008"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    list.append(rua['1'])

    return json.dumps(list)

@app.route("/jiangjin/7d_2")
def jiangjin2():

    list=[]

    url = "https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E9%87%8D%E5%BA%86&city=%E9%87%8D%E5%BA%86&county=%E6%B1%9F%E6%B4%A5&callback=jQuery111307596638576679418_1564706624996&_=1564706625008"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    list.append(rua['2'])

    return json.dumps(list)

@app.route("/jiangjin/7d_3")
def jiangjin3():

    list=[]

    url = "https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=%E9%87%8D%E5%BA%86&city=%E9%87%8D%E5%BA%86&county=%E6%B1%9F%E6%B4%A5&callback=jQuery111307596638576679418_1564706624996&_=1564706625008"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    response = requests.get(url)

    data = response.text

    data = json.loads(data[data.find('{'):-1])


    rua = data["data"]["forecast_24h"]

    list.append(rua['3'])

    return json.dumps(list)

@app.route("/guandu/video/select")
def select_video():
    id = flask.request.args.get("id")
    if id == "1":
        return '[{"url": "%s"}]' % 'http://tylin-js.com.cn/guandu/video/%E6%A0%B7%E6%9D%BF1.mp4'
    elif id == "2":
        return '[{"url": "%s"}]' % 'http://tylin-js.com.cn/guandu/video/%E6%A0%B7%E6%9D%BF2.mp4'

    elif id == "3":
        return '[{"url": "%s"}]' % 'http://tylin-js.com.cn/guandu/video/%E6%A0%B7%E6%9D%BF3.mp4'

    elif id == "4":
        return '[{"url": "%s"}]' % 'http://tylin-js.com.cn/guandu/video/%E6%A0%B7%E6%9D%BF4.mp4'

    elif id == "5":
        return '[{"url": "%s"}]' % 'http://tylin-js.com.cn/guandu/video/%E6%A0%B7%E6%9D%BF5.mp4'

    elif id == "6":
        return '[{"url": "%s"}]' % 'http://tylin-js.com.cn/guandu/video/%E6%A0%B7%E6%9D%BF6.mp4'

    elif id == "7":
        return '[{"url": "%s"}]' % 'http://tylin-js.com.cn/guandu/video/%E6%A0%B7%E6%9D%BF7.mp4'

    else:
        return '[{"url": "%s"}]' % 'http://tylin-js.com.cn/guandu/video/%E5%90%8E%E6%B5%87%E5%B8%A6%E6%96%BD%E5%B7%A5%E5%8A%A8%E7%94%BB.mp4'

@app.route("/guandu/video_live/select")
def select_video_live():
    id = flask.request.args.get("id")
    if id == "1":
        return '[{"url": "%s"}]' % 'http://hls01open.ys7.com/openlive/a3d1775087164795bc85bd4aa5a32e12.hd.m3u8'
    elif id == "2":
        return '[{"url": "%s"}]' % 'http://hls01open.ys7.com/openlive/ef316c1bef104203a2cbc265ffca65e8.hd.m3u8'

    elif id == "3":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'

    elif id == "4":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'

    elif id == "5":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'

    else:
        return '[{"url": "%s"}]' % 'http://hls01open.ys7.com/openlive/3e5ae0fa57ba48658ca1347405141c66.hd.m3u8'

@app.route("/guandu/model/select")
def select_model():
    id = flask.request.args.get("id")
    if id == "1":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=jYnMZf'
    elif id == "2":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=QbMZZf'

    elif id == "3":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=nmEfue'

    elif id == "4":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=YZfMVf'

    elif id == "5":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=MJrURb'

    elif id == "6":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=36Nr2e'

    elif id == "7":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=VfQF7n'

    elif id == "8":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=Bb2EFv'

    elif id == "9":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=RFvIry'

    elif id == "10":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=juYNzq'

    elif id == "11":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=uuMbIz'

    elif id == "12":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=eENFfq'

    elif id == "13":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=36nuau'

    elif id == "14":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=uiY3Ar'

    elif id == "15":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=FjIJrq'

    elif id == "16":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=JVBrMf'

    elif id == "17":
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=If2uye'

    elif id == "18":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'

    elif id == "19":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'

    elif id == "20":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'

    elif id == "21":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'

    elif id == "22":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'

    elif id == "23":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'

    elif id == "24":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'

    elif id == "25":
        return '[{"url": "%s"}]' % 'http://183.66.213.82:8888/weather_qq/warning/upgrading'


    else:
        return '[{"url": "%s"}]' % 'http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=RJV7f2'

@app.route('/shenzhen/weather_bdip')
def weather_bdip():

    return flask.render_template("index.html")

@app.route("/warning/upgrading")
def warning_upgrading():
    return flask.render_template("2.html")








application = app
if __name__ == '__main__':
	app.run(host="0.0.0.0",port=8808, debug=True)