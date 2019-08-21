#coding:utf-8
from flask import request
import mysql.connector
import json
import time

conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='shenzhen_event',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()

#数据库查询语句(通用)

complete_data = 'SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where finish_time is not null '
in_plan_data = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time)<-3 and finish_time is null"
near_data = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time) between -3 and 0 and finish_time is null"
late_data = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time)>0 and finish_time is null"


complete_dpi = 'SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where finish_time is not null and event.dpi='
in_plan_dpi = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time)<-3 and finish_time is null and event.dpi="
near_dpi = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time) between -3 and 0 and finish_time is null and event.dpi="
late_dpi = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name,email from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time)>0 and finish_time is null and event.dpi="







#筛选
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

def late():
    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]

    if dpi== "0":

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time) >0 LIMIT " + str((page - 1) * 10) + ',10'
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

            dict = {"id": id, 'event_name': event_name, 'start_plan':start_plan ,'plan_time': plan_time, 'finish_time': finish_time, 'state': state,
                    'department': department,"contector":contector}

            list.append(dict)


    else:

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where event.dpi=" + dpi + " and datediff(CURRENT_DATE , plan_time) >0 LIMIT " + str((page - 1) * 10) + ',10'
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

            dict = {"id": id, 'event_name': event_name, 'start_plan': start_plan, 'plan_time': plan_time,
                    'finish_time': finish_time, 'state': state, 'department': department, "contector": contector}

            list.append(dict)

    return json.dumps(list)

def near():
    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]

    if dpi== "0":

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time) between -3 and 0 LIMIT " + str((page - 1) * 10) + ',10'
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

            dict = {"id": id, 'event_name': event_name, 'start_plan':start_plan ,'plan_time': plan_time, 'finish_time': finish_time, 'state': state,
                    'department': department,"contector":contector}

            list.append(dict)


    else:

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where event.dpi=" + dpi + " and datediff(CURRENT_DATE , plan_time) between -3 and 0 LIMIT " + str((page - 1) * 10) + ',10'
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

def complete():

    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]



    if dpi=="0":

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where finish_time is not null LIMIT " + str(page) + ',10'
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

            dict = {"id": id, 'event_name': event_name, 'start_plan':start_plan ,'plan_time': plan_time, 'finish_time': finish_time, 'state': state,
                    'department': department,"contector":contector}

            list.append(dict)

    else:

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where event.dpi=" + dpi + " and finish_time is not null LIMIT " + str((page - 1) * 10) + ',10'
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

            dict = {"id": id, 'event_name': event_name, 'start_plan':start_plan ,'plan_time': plan_time, 'finish_time': finish_time, 'state': state,
                    'department': department,"contector":contector}

            list.append(dict)

    return json.dumps(list)

def in_plan():

    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]

    if dpi=="0":

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time)<-3 LIMIT " + str((page - 1) * 10) + ',10'
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

            dict = {"id": id, 'event_name': event_name, 'start_plan':start_plan ,'plan_time': plan_time, 'finish_time': finish_time, 'state': state,
                    'department': department,"contector":contector}

            list.append(dict)

    else:
        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where event.dpi=" + dpi + " and datediff(CURRENT_DATE , plan_time)<-3 LIMIT " + str((page - 1) * 10) + ',10'
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

            dict = {"id": id, 'event_name': event_name, 'start_plan': start_plan, 'plan_time': plan_time,
                    'finish_time': finish_time, 'state': state, 'department': department, "contector": contector}

            list.append(dict)


    return json.dumps(list)

def page():
    data = request.get_json()
    dpi = data["dpi"]

    if dpi == "0":

        # 查找已完成:
        cursor.execute(complete_data)
        complete = cursor.fetchall()
        # 查找计划中:
        cursor.execute(in_plan_data)
        in_plan = cursor.fetchall()
        # 查找临近:
        cursor.execute(near_data)
        near = cursor.fetchall()
        # 查找滞后:
        cursor.execute(late_data)
        late = cursor.fetchall()


        count_dict = {"total":len(late)+len(near)+len(in_plan)+len(complete),"late":len(late),"near":len(near),"in_plan":len(in_plan),"complete":len(complete)}

        count_list =[]

        count_list.append(count_dict)

    else:
        # 查找已完成:
        cursor.execute(complete_dpi+dpi)
        complete = cursor.fetchall()
        # 查找计划中:
        cursor.execute(in_plan_dpi+dpi)
        in_plan = cursor.fetchall()
        # 查找临近:
        cursor.execute(near_dpi+dpi)
        near = cursor.fetchall()
        # 查找滞后:
        cursor.execute(late_dpi+dpi)
        late = cursor.fetchall()

        count_dict = {"total":len(late)+len(near)+len(in_plan)+len(complete),"late":len(late),"near":len(near),"in_plan":len(in_plan),"complete":len(complete)}

        count_list = []

        count_list.append(count_dict)


    return json.dumps(count_list)
