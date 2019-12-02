#coding:utf-8
from flask import Flask,request,render_template
import mysql.connector
import json
import time
import datetime
import requests
from dateutil.relativedelta import relativedelta
import sys

def canlian_index_safe():

    # 安全部分

    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/safety.action"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]


    list_safe = []
    for i in dataList_1:
        if i["rectificate"] == "是":
            list_safe.append(i)

    # 质量部分

    url_2 = "http://www.tylinbim.com/4DAnalog/ltyCL/quality.action"
    res_2 = requests.get(url_2)
    data_2 = json.loads(res_2.text)
    dataList_2 = data_2["data"]

    list_quality = []
    for j in dataList_2:
        if j["rectificate"] == "是":
            list_quality.append(j)





    y = [
        {"name":"问题总数","data": [len(dataList_1),len(dataList_2)]},
        {"name":"已解决","data": [len(list_safe),len(list_quality)]}
    ]
    x = ["安全问题","质量问题"]

    dict = {"y": y, "x": x}

    return json.dumps(dict)