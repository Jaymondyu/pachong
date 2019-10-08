# -- coding: utf-8 --
import flask
from flask import request
import json
import requests
import operator
import datetime
import sys
from dateutil.relativedelta import relativedelta

reload(sys)
sys.setdefaultencoding('utf8')

url_1 = "http://www.tylinbim.com/wui/qualityProList"
res_1 = requests.get(url_1)
data_1 = json.loads(res_1.text)
dataList_1 = data_1["data"]

datetime_now = datetime.datetime.now().strftime("%Y-%m-%d")
today = datetime.datetime.strptime(datetime_now,'%Y-%m-%d')

d30 = []
d30_60 = []
d60_90 = []
d90_120 = []
d120 = []
unsolved = []

for i in dataList_1:
    if i["rectificate"] == "是":
        pass
    else:
        unsolved.append(i)
        day = str(today - datetime.datetime.strptime(i["checkTime"],'%Y-%m-%d'))
        if day == "0:00:00":
            day = 0
        elif day == "1 day, 0:00:00":
            day = 1
        else:
            day = int(day.replace(" days, 0:00:00",""))
        if day<=30:
            d30.append(i)
        elif 30<day<=60:
            d30_60.append(i)
        elif 60<day<=90:
            d60_90.append(i)
        elif 90<day<=120:
            d90_120.append(i)
        elif 120<day:
            d120.append(i)

dict = {
        "data":{
            "x":["<30","30~60","60~90","90~120",">120"],
            "unsolved":[len(d30),len(d30_60),len(d60_90),len(d90_120),len(d120)],
            "total":[len(d30),len(d30)+len(d30_60),len(d30)+len(d30_60)+len(d60_90),len(d30)+len(d30_60)+len(d60_90)+len(d90_120),len(d30)+len(d30_60)+len(d60_90)+len(d90_120)+len(d120)]
        }
}


print dict
