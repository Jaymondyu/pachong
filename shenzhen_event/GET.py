#coding:utf-8
import mysql.connector
import json
import datetime

conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='shenzhen_event',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()


#数据库查询语句(通用)

complete_data = 'SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where finish_time is not null '
in_plan_data = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time)<-3 and finish_time is null"
near_data = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time) between -3 and 0 and finish_time is null"
late_data = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time)>0 and finish_time is null"


#GET页面函数:

# 统计:
def count():

    #查找已完成:
    cursor.execute(complete_data)
    complete = cursor.fetchall()
    #查找计划中:
    cursor.execute(in_plan_data)
    in_plan = cursor.fetchall()
    # 查找临近:
    cursor.execute(near_data)
    near = cursor.fetchall()
    # 查找滞后:
    cursor.execute(late_data)
    late = cursor.fetchall()
    #统一封装:
    count_dict = {"late":len(late),"near":len(near),"in_plan":len(in_plan),"complete":len(complete)}
    count_list =[]
    count_list.append(count_dict)

    return json.dumps(count_list)

# 日期:
def date():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d')

    return current_time

# 滞后邮件收件人:
def email_late():


    cursor.execute(late_data)

    late = cursor.fetchall()
    list=[]
    for i in late:
        event_name=i[1]
        department = i[5]
        email = i[7]

        list_1 = [event_name,email,department]
        list.append(list_1)
    return list

# 临近邮件收件人
def email_near():


    cursor.execute(near_data)

    near = cursor.fetchall()
    list = []
    for i in near:
        event_name=i[1]
        department = i[5]
        email = i[7]

        list_1 = [event_name,email,department]
        list.append(list_1)
    return list

