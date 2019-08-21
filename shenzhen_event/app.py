#coding:utf-8
from flask import Flask,request
import mysql.connector
import time
import json
import GET
import POST_select
import POST_edit

conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='shenzhen_event',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()


#数据库查询语句(通用)

complete_data = 'SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where finish_time is not null '
in_plan_data = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time)<-3 and finish_time is null"
near_data = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time) between -3 and 0 and finish_time is null"
late_data = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time)>0 and finish_time is null"


app = Flask(__name__)



@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route("/show")
def show():
    return app.send_static_file('show.html')

# GET页面
@app.route('/table/count')
def count():
    return(GET.count())

@app.route("/table/date")
def date():
    return (GET.date())

@app.route('/table/email_late')
def email_late():
    return(json.dumps(GET.email_late()))

@app.route('/table/email_near')
def email_near():
    return (json.dumps(GET.email_near()))

# POST页面


# 修改页面
@app.route("/table/insert" ,methods=["POST"])
def insert():
    return(POST_edit.insert())

@app.route("/table/cancel", methods=["POST"])
def cancel():
    return (POST_edit.cancel())

@app.route("/table/delete", methods=["POST"])
def delete():
    return (POST_edit.delete())

@app.route("/table/change", methods=["POST"])
def change():
    return (POST_edit.change())


#筛选页面

@app.route('/table/page',methods=['POST'])
def page():
    return POST_select.page()

@app.route('/table',methods=["POST"])
def table():
    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]

    if dpi== "0":


        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id LIMIT "+ str((page-1)*10)+',10'

        cursor.execute(table)

        result = cursor.fetchall()

        list = []

        for i in result:

            id = i[0]
            event_name = i[1]
            start_plan = i[2].strftime('%Y-%m-%d')
            plan_time = i[3].strftime('%Y-%m-%d')
            finish_time = i[4]

            localtime = time.strftime("%Y-%m-%d", time.localtime())

            plan_time_trans = time.mktime(time.strptime(plan_time, "%Y-%m-%d"))
            localtime_trans = time.mktime(time.strptime(localtime, "%Y-%m-%d"))

            time_dis = localtime_trans - plan_time_trans

            state = int(time_dis) / 86400

            if finish_time == None:
                finish_time = i[4]

            else:
                finish_time = i[4].strftime('%Y-%m-%d')
                state = 999999

            department = i[5]
            contector = i[6]
            if contector == "":
                contector = "无"

            dict = {"id": id, 'event_name': event_name, 'start_plan':start_plan,'plan_time': plan_time, 'finish_time': finish_time, 'state': state,'department': department,"contector":contector}

            list.append(dict)

    else:

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where event.dpi=" + dpi + " LIMIT "+ str((page-1)*10)+',10'
        cursor.execute(table)

        result = cursor.fetchall()

        list = []

        for i in result:

            id = i[0]
            event_name = i[1]
            start_plan = i[2].strftime('%Y-%m-%d')
            plan_time = i[3].strftime('%Y-%m-%d')
            finish_time = i[4]

            localtime = time.strftime("%Y-%m-%d", time.localtime())

            plan_time_trans = time.mktime(time.strptime(plan_time, "%Y-%m-%d"))
            localtime_trans = time.mktime(time.strptime(localtime, "%Y-%m-%d"))

            time_dis = localtime_trans - plan_time_trans

            state = int(time_dis) / 86400

            if finish_time == None:
                finish_time = i[4]

            else:
                finish_time = i[4].strftime('%Y-%m-%d')
                state = 999999

            department = i[5]
            contector = i[6]
            if contector == "":
                contector = "无"

            dict = {"id": id, 'event_name': event_name, 'start_plan':start_plan,'plan_time': plan_time, 'finish_time': finish_time, 'state': state,'department': department,"contector":contector}

            list.append(dict)

    return json.dumps(list)


@app.route('/table/late',methods=["POST"])
def late():
    return POST_select.late()

@app.route('/table/near',methods=["POST"])
def near():
    return POST_select.near()

@app.route('/table/complete',methods=["POST"])
def complete():
    return POST_select.complete()

@app.route('/table/in_plan',methods=["POST"])
def in_plan():
    return POST_select.in_plan()

application = app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888, debug=True)
