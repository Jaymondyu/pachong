from flask import Flask,request
import mysql.connector
import json
import datetime
import time

app = Flask(__name__)

conn = mysql.connector.connect( host= '127.0.0.1',user= 'root',password ='plokijuh9',database ='j') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()

@app.route('/table')
def hello_world():
    table = "SELECT test_alarm.id,event_name, plan_time, finish_time, department,name from test_alarm JOIN person ON test_alarm.dpi=person.id"

    cursor.execute(table)

    result = cursor.fetchall()

    list = []

    for i in result:

        id = i[0]
        event_name = i[1]
        plan_time = i[2].strftime('%Y-%m-%d')
        finish_time = i[3]

        localtime = time.strftime("%Y-%m-%d", time.localtime())

        plan_time_trans = time.mktime(time.strptime(plan_time, "%Y-%m-%d"))
        localtime_trans = time.mktime(time.strptime(localtime, "%Y-%m-%d"))

        time_dis = localtime_trans - plan_time_trans

        state = int(time_dis) / 86400

        if finish_time == None:
            finish_time = i[3]

        else:
            finish_time = i[3].strftime('%Y-%m-%d')
            state = 999999

        department = i[4]
        contector = i[5]
        if contector == "":
            contector = "无"

        dict = {"id": id, 'event_name': event_name, 'plan_time': plan_time, 'finish_time': finish_time, 'state': state,
                'department': department,"contector":contector}

        list.append(dict)

    return json.dumps(list)

@app.route("/table/insert" ,methods=["POST"])
def insert():
    data = request.get_json()

    event_name = data['event_name']
    plan_time = data["plan_time"]
    finish_time = data["finish_time"]
    dpi = data["dpi"]

    if finish_time == "":
        finish_time = 'Null'

    if finish_time == 'Null':

        sql = "INSERT INTO test_alarm (event_name, plan_time, finish_time, dpi) VALUES ('%s','%s',%s,%d)"% (event_name,plan_time,finish_time,dpi)

    else:

        sql = "INSERT INTO test_alarm (event_name, plan_time, finish_time, dpi) VALUES ('%s','%s','%s',%d)" % (event_name, plan_time, finish_time, dpi)


    cursor.execute(sql)
    conn.commit()

    table = "SELECT test_alarm.id,event_name, plan_time, finish_time, department,name from test_alarm JOIN person ON test_alarm.dpi=person.id"

    cursor.execute(table)

    result = cursor.fetchall()

    list = []

    for i in result:

        id = i[0]
        event_name = i[1]
        plan_time = i[2].strftime('%Y-%m-%d')
        finish_time = i[3]

        localtime = time.strftime("%Y-%m-%d", time.localtime())

        plan_time_trans = time.mktime(time.strptime(plan_time, "%Y-%m-%d"))
        localtime_trans = time.mktime(time.strptime(localtime, "%Y-%m-%d"))

        time_dis = localtime_trans - plan_time_trans

        state = int(time_dis) / 86400

        if finish_time == None:
            finish_time = i[3]

        else:
            finish_time = i[3].strftime('%Y-%m-%d')
            state = 999999

        department = i[4]
        contector = i[5]
        if contector == "":
            contector = "无"

        dict = {"id": id, 'event_name': event_name, 'plan_time': plan_time, 'finish_time': finish_time, 'state': state,
                'department': department, "contector": contector}

        list.append(dict)

    return json.dumps(list)

@app.route("/table/cancel" ,methods=["POST"])
def cancel():
    data = request.get_json()
    id = data["id"]

    cancel =


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
