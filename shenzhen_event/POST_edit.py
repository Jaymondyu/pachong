#coding:utf-8
from flask import request
import mysql.connector
import datetime
import POST_select

conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='shenzhen_event',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()


# 修改
def insert():
    data = request.get_json()

    event_name = data['event_name']
    start_plan = data["start_plan"]
    plan_time = data["plan_time"]
    finish_time = data["finish_time"]
    dpi = data["dpi"]

    if finish_time == "":
        finish_time = 'Null'

    if finish_time == 'Null':

        sql = "INSERT INTO event (event_name,start_plan ,plan_time, finish_time, dpi) VALUES ('%s','%s','%s',%s,%d)"% (event_name,start_plan,plan_time,finish_time,dpi)

    else:

        sql = "INSERT INTO event (event_name, start_plan,plan_time, finish_time, dpi) VALUES ('%s','%s','%s','%s',%d)" % (event_name,start_plan ,plan_time, finish_time, dpi)


    cursor.execute(sql)
    conn.commit()

    return (POST_select.table())

def cancel():
    data = request.get_json()
    id = data["id"]

    current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    cancel = "UPDATE event SET finish_time =" + "'"+current_time+"'" + "where id=" + "'" +id+ "'"
    cursor.execute(cancel)
    conn.commit()

    return (POST_select.table())

def delete():
    data = request.get_json()
    id = data["id"]

    delete = "DELETE FROM event WHERE id=" + "'" +id+ "'"
    cursor.execute(delete)
    conn.commit()

    return (POST_select.table())

def change():


    data = request.get_json()
    id = data["id"]
    start_plan = data["start_plan"]
    event_name = data['event_name']
    plan_time = data["plan_time"]
    dpi = data["dpi"]


    change = "UPDATE event SET event_name ='%s',start_plan ='%s',plan_time ='%s',dpi ='%s'where id='%s'"%(event_name,start_plan,plan_time,dpi,id)
    cursor.execute(change)
    conn.commit()

    return (POST_select.table())

