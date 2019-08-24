#coding:utf-8
from flask import Flask,request,render_template
import mysql.connector
import json
import time
import datetime
import requests

conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='openplatform',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()

app = Flask(__name__)

# 江津大屏
# 江津驾驶舱接口

# 天气
@app.route("/jiangjin/index/weather")
def index_weather():
    #数据库查询
    sql_weather = "select pm2p5,pm10,noise,temperature from environment order by id desc LIMIT 1"
    cursor.execute(sql_weather)
    enviroment = cursor.fetchall()
    #获取剩余天数
    days = requests.get("http://183.66.213.82:8888/shenzhen/date/begin?d=2019-02-19")
    days = days.text
    days = int(days[10:-2])
    #整合
    list={
        "pm2.5":enviroment[0][0],
        "pm10":enviroment[0][1],
        "noise":enviroment[0][2],
        "temperature":enviroment[0][3],
        "days":days
    }
    return json.dumps(list)
# 人员统计
@app.route("/jiangjin/index/renyuan")
def index_renyuan():
    #数据库查询
    sql_renyuan = """
                    SELECT
                        count(*) AS y,
                        DATE_FORMAT(attendancetime, '%Y-%m-%d') AS x,
                    case 
                    when department in ("重庆建工住宅建设有限公司","林同棪【重庆】国际工程技术有限公司")then 1 
                    when department in  ("重庆正旋基础有限公司","重庆名庆防水工程有限公司","重庆力杰消防工程有限公司" )then 3
                    when department = "重庆联文建筑劳务有限公司" then 2
                    end s
                    FROM
                        (select name,department, DATE_FORMAT(attendancetime, '%Y-%m-%d') as attendancetime from access
                    WHERE
                        DATE_FORMAT(attendancetime, '%Y-%m-%d') BETWEEN DATE_SUB(CURRENT_DATE, INTERVAL 6 DAY) AND DATE_FORMAT(CURRENT_DATE, '%Y-%m-%d')
                    AND entry = 1
                    group by 1,2,3
                    
                    ) as a
                    GROUP BY s,x
                    ORDER BY s
                """
    cursor.execute(sql_renyuan)
    renyuan = cursor.fetchall()
    list_x = []
    list_1 = []
    list_2 = []
    list_3 = []
    for i in renyuan:
        list_x.append(i[1])
        if i[2] == 1:
            list_1.append(i[0])
        elif i[2] == 2:
            list_2.append(i[0])
        elif i[2] == 3:
            list_3.append(i[0])

    dict = {
        "x":list_x[0:7],
        "y":[{"name":"管理人员","data":list_1},{"name":"劳务人员","data":list_2},{"name":"专业分包","data":list_3}]

    }


    return json.dumps(dict)
# 质量问题与安全问题
@app.route("/jiangjin/index/zhiliang")
def index_zhiliang():
    sql_zhiliang = "select date,zhiliang,anquan from jiangjin_screen where date is not NULL order by id desc LIMIT 5"
    cursor.execute(sql_zhiliang)
    zhiliang = cursor.fetchall()

    list_x = []
    list_zhiliang = []
    list_anquan = []

    for i in zhiliang:
        list_x.append(i[0])
        list_zhiliang.append(i[1])
        list_anquan.append(i[2])

    dict={
        "x":list_x,
        "y":[{"name":"质量问题","data":list_zhiliang},{"name":"安全问题","data":list_anquan}]
    }


    return json.dumps(dict)
# 进度
@app.route("/jiangjin/index/jindu")
def jindu():
    sql_jindu = "select tujian,xuanwazhuang,wakongzhuang,jidian,muqiang,jingzhuang,shiwaigongcheng from jiangjin_screen where tujian is not NULL order by id desc LIMIT 1"
    cursor.execute(sql_jindu)
    jindu = cursor.fetchall()
    list = [{
        "1": jindu[0][0],
        "2": jindu[0][1],
        "3": jindu[0][2],
        "4": jindu[0][3],
        "5": jindu[0][4],
        "6": jindu[0][5],
        "7": jindu[0][6]
    }]
    return json.dumps(list)

# 人员管理接口
# 管理人员
@app.route("/jiangjin/renyuan/guanli")
def guanli():
    sql_guanli = """SELECT 
            access.name, personnel.role, personnel.telephone, if(entry=1,'进场','出场') as entry, DATE_FORMAT(attendancetime,'%Y-%m-%d %H:%i:%s') as attendancetime, access.department 
            from access,personnel 
            where access.name=personnel.name 
            and 
            DATE_FORMAT(attendancetime,'%Y-%m-%d') = date_format(CURRENT_DATE,'%Y-%m-%d') 
            AND
             access.department in ('重庆建工住宅建设有限公司','林同棪【重庆】国际工程技术有限公司')"""

    cursor.execute(sql_guanli)
    guanli = cursor.fetchall()
    list = []
    for i in guanli:
        dict = {
            "name": i[0],
            "type": i[1],
            "tel": i[2],
            "state": i[3],
            "time": i[4],
            "company": i[5]
        }
        list.append(dict)

    return json.dumps(list)
# 劳务人员
@app.route("/jiangjin/renyuan/laowu")
def laowu():
    sql_laowu = """
                SELECT 
                name, department,if(entry=1,'进场','出场') as entry, DATE_FORMAT(attendancetime,'%Y-%m-%d %H:%i:%s') as attendancetime 
                from access 
                where 
                DATE_FORMAT(attendancetime,'%Y-%m-%d') = date_format(CURRENT_DATE,'%Y-%m-%d') 
                AND 
                department in ('重庆联文建筑劳务有限公司')
    """
    cursor.execute(sql_laowu)
    guanli = cursor.fetchall()
    list = []
    for i in guanli:
        dict = {
            "name": i[0],
            "state": i[2],
            "time": i[3],
            "company": i[1]
        }
        list.append(dict)

    return json.dumps(list)











application = app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888, debug=True)