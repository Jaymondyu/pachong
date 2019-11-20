#coding:utf-8
import mysql.connector

import json
import urllib3
import sys
reload(sys)
sys.setdefaultencoding('utf8')



conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='shenzhen_event',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()

# aaa="select sum(day_out) from yuelai__tushifang where date <'2019-10-21'"
# cursor.execute(aaa)
# info = cursor.fetchall()
# conn.close()
# print info


search = "select * from yuelai_tushifang"
cursor.execute(search)
info = cursor.fetchall()
conn.close()

print info

# for i in info:
#     i = list(i)
#     d1 = str(i[0]).encode("utf-8")
#     d2 = i[1]
#     d3 = i[2].encode("utf-8")
#     d4 = i[3]
#     d5 = i[4]
#     d6 = i[5]
#     d7 = i[6]
#     d8 = i[7].encode("utf-8")
#     d9 = i[8].encode("utf-8")
#     d10 = i[9].encode("utf-8")
#     d11 = i[10].encode("utf-8")
#
#
#     dict = {
#     "date" :str(d1.replace("/","-").replace(" 00:00:00","")),
#     "car_amount" :int(d2),
#     "zhachang" :str(d3),
#     "distance" :str(d4),
#     "digger_amount" :int(d5),
#     "day_car_out" :int(d6),
#     "day_out" :int(d7),
#     "manager" : str(d8),
#     "file_path" :str(d9),
#     "ps" :str(d10),
#     "area" :str(d11)
#             }
#     print dict["date"]
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5733.400 QQBrowser/10.2.2019.400'
#     }
#
#     data = json.dumps(dict).encode("utf-8")
#     url = "http://172.168.10.22:5000/insert"
#
#     http = urllib3.PoolManager()
#     r = http.request(
#     "POST",
#     url,
#     body = data,
#     headers = {
#         'x-env-code':'mafutian',
#         'content-type':'application/json;charset=UTF-8'
#     }
#     )


