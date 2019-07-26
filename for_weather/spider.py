#coding:utf-8
import urllib.request
import re
import json

def weather():

    day = []
    hours = []

    url = 'http://www.weather.com.cn/weather1d/101290101.shtml'

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    }

    request = urllib.request.Request(url,headers=headers)

    response = urllib.request.urlopen(url)

    data = response.read().decode("utf-8")

    data_weather = re.findall(r"\"7d\":\[(.*?)]}",data,re.S)


    # print(json.loads("["+data_weather[0]+"]")[0])

    for i in json.loads("["+data_weather[0]+"]"):
        for l in i:
            arr = l.split(',')
            day.append([arr[0],arr[2],arr[3]])

    return day

print(weather())