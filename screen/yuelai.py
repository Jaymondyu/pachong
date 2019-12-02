#coding:utf-8
from flask import Flask,request,render_template
import mysql.connector
import json
import time
import datetime
import requests
from dateutil.relativedelta import relativedelta
import sys
from flask import Blueprint
reload(sys)
sys.setdefaultencoding('utf8')

yuelai = Blueprint('yuelai', __name__,static_url_path="http://183.66.213.82:8888/screen/static/js_yuelai/")


# 悦来会展总部基地项目大屏
# 驾驶舱
# @yuelai.route("/")
# def index():
#     return render_template("index_yuelai.html")
# 天气
@yuelai.route("/index/weather")
def yuelai_index_weather():
    # 数据库查询
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='yuelai_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_weather = "select pm2p5,pm10,noise,temperature from environment order by id desc LIMIT 1"
    cursor.execute(sql_weather)
    enviroment = cursor.fetchall()
    # 获取剩余天数
    days = requests.get("http://183.66.213.82:8888/shenzhen/date/begin?d=2019-07-01")
    days = days.text
    days = int(days[10:-2])
    # 整合
    list = {"data":{
        "pm2p5": enviroment[0][0],
        "pm10": enviroment[0][1],
        "noise": enviroment[0][2],
        "temperature": enviroment[0][3],
        "days": days
    }}
    conn.close()
    return json.dumps(list)
#资产统计
@yuelai.route("/index/zichan")
def yuelai_index_renyuan():
    dict = {
        "x":["8月第1周","8月第2周","8月第3周","8月第4周"],
        "y":[{"name":"计划产值","data":[200,400,450,500]},{"name":"实际产值","data":[150,350,400,450]}]
    }
    return json.dumps(dict)
# 进度
@yuelai.route("/index/jindu")
def yuelai_jindu():

    list = [
        {"data": 0,
         "name":"结构工程"},
        {"data":0,
         "name":"建筑工程"},
        {"data":0,
         "name":"机电工程"},
        {"data": 0,
         "name":"幕墙工程"},
        {"data":0,
         "name":"精装工程"},
        {"data": 0,
         "name":"景观工程"}
    ]
    return json.dumps(list)

# 项目概况
@yuelai.route("/index/intro")
def yuelai_intro():
    dict = {"data":{
        "data": """    项目紧邻悦来国博会展中心及会展公园，是国博会展中心重要的配套项目。项目以实现绿色建筑三星、LEED金级标准为设计目标，旨在打造一个集智能、绿色、时尚为一体的具有新区特色和时代风貌的文化艺术城市综合体，成为悦来会展城重要地标性建筑，也将成为绿色建筑、智能建筑的典范工程。
    项目总用地面积20904.00㎡，容积率6.0，建筑密度40%，绿地率30%.总建筑面积204204.60 ㎡，其中计容建筑面积125424.00㎡，地上建筑面积162609.28 ㎡，地下建筑面积41595.32 ㎡。建筑最高195.67m。由一栋23层的高层塔楼、一栋43层的超高层塔楼及裙房组成，地下吊2层，负6层为设备用房及车库。高层塔楼功能为雅辰酒店，约384间客房；超高层部分吊1层至34层功能为办公（其中1层、17层为酒店大堂），35层至43层为洲际集团旗下英迪格酒店，约200间客房，裙房为配套商业。              
    """
    }}
    return json.dumps(dict)
# 参建单位
@yuelai.route("/index/company")
def yuelai_company():
    list = {"data":[
        {
            "unit": "建设单位",
            "company": "重庆悦瑞文化旅游发展有限公司"
        },
        {
            "unit": "设计单位",
            "company": "重庆博建建筑规划设计有限公司"
        }, {
            "unit": "施工总包单位",
            "company": "中国建筑第八工程局有限公司"
        }, {
            "unit": "监理单位",
            "company": "林同棪（重庆）国际工程技术有限公司"
        }, {
            "unit": "BIM咨询",
            "company": "林同棪（重庆）国际工程技术有限公司"
        }, {
            "unit": "监测单位",
            "company": "重庆市市政设计研究院"
        }, {
            "unit": "跟审单位",
            "company": "中京华（北京）工程咨询有限公司"
        }
    ]}
    return json.dumps(list)
# 效果图预览
@yuelai.route("/index/pic")
def yuelai_pic():
    list={
       "data":{"data":[{"url":"http://183.66.213.82:8888/screen/static/yuelai_pic/1.png"},{"url":"http://183.66.213.82:8888/screen/static/yuelai_pic/2.png"},{"url":"http://183.66.213.82:8888/screen/static/yuelai_pic/3.png"}]}
    }
    return json.dumps(list)
# 无人机地址
@yuelai.route("/index/wurenji")
def yuelai_wurenji():
    dict = {"data":
        {"data":"https://720yun.com/t/e8vknmdlr7l"}
    }
    return json.dumps(dict)
# 模型(左)地址
@yuelai.route("/index/iframe_left")
def yuelai_iframe_left():
    dict = {"data":
        {"data":"http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=UnIv6b"}
    }
    return json.dumps(dict)
# 模型(右)地址
@yuelai.route("/index/iframe_right")
def yuelai_iframe_right():
    dict = {"data":
        {"data":"http://www.tylinbim.com/4DAnalog/s.action?url=vq6FV3"}
    }
    return json.dumps(dict)




# 计划追踪

# 修改
# 修改
@yuelai.route("/event/table/insert" ,methods=["POST"])
def insert():
    data = request.get_json()
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    event_name = data['event_name']
    start_plan = data["start_plan"]
    plan_time = data["plan_time"]
    finish_time = data["finish_time"]
    dpi = data["dpi"]

    if finish_time == "":
        finish_time = 'Null'

    if finish_time == 'Null':

        sql = "INSERT INTO yuelai_event (event_name,start_plan ,plan_time, finish_time, dpi) VALUES ('%s','%s','%s',%s,%d)"% (event_name,start_plan,plan_time,finish_time,dpi)

    else:

        sql = "INSERT INTO yuelai_event (event_name, start_plan,plan_time, finish_time, dpi) VALUES ('%s','%s','%s','%s',%d)" % (event_name,start_plan ,plan_time, finish_time, dpi)


    cursor.execute(sql)
    conn.commit()

    table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id"

    cursor.execute(table)

    result = cursor.fetchall()
    conn.close()
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

@yuelai.route("/event/table/cancel" ,methods=["POST"])
def cancel():
    data = request.get_json()
    id = data["id"]
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    cancel = "UPDATE yuelai_event SET finish_time =" + "'"+current_time+"'" + "where id=" + "'" +id+ "'"
    cursor.execute(cancel)
    conn.commit()

    table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id"

    cursor.execute(table)

    result = cursor.fetchall()
    conn.close()
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

@yuelai.route("/event/table/delete" ,methods=["POST"])
def delete():
    data = request.get_json()
    id = data["id"]
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    delete = "DELETE FROM yuelai_event WHERE id=" + "'" +id+ "'"
    cursor.execute(delete)
    conn.commit()

    table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id"

    cursor.execute(table)

    result = cursor.fetchall()
    conn.close()
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

@yuelai.route("/event/table/change" ,methods=["POST"])
def change():


    data = request.get_json()
    id = data["id"]
    start_plan = data["start_plan"]
    event_name = data['event_name']
    plan_time = data["plan_time"]
    dpi = data["dpi"]
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()

    change = "UPDATE yuelai_event SET event_name ='%s',start_plan ='%s',plan_time ='%s',dpi ='%s'where id='%s'"%(event_name,start_plan,plan_time,dpi,id)
    cursor.execute(change)
    conn.commit()




    table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id"

    cursor.execute(table)

    result = cursor.fetchall()
    conn.close()
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


# 展示
# 全部
@yuelai.route('/event/table',methods=["POST"]) #dpi,page
def table():
    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    if dpi== "0":


        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id LIMIT "+ str((page-1)*10)+',10'

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

        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id where yuelai_event.dpi=" + dpi + " LIMIT "+ str((page-1)*10)+',10'

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
    final_dict = {"data":list}
    conn.close()
    return json.dumps(final_dict)
# 滞后
@yuelai.route('/event/table/late',methods=["POST"]) #dpi,page
def late():
    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    if dpi== "0":

        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id where datediff(CURRENT_DATE , plan_time) >0 and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
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

        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id where yuelai_event.dpi=" + dpi + " and datediff(CURRENT_DATE , plan_time) >0 and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
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
    final_dict = {"data": list}
    conn.close()
    return json.dumps(final_dict)
# 临近
@yuelai.route('/event/table/near',methods=["POST"]) #dpi,page
def near():
    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    if dpi== "0":

        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id where datediff(CURRENT_DATE , plan_time) between -3 and 0  and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
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

        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id where event.dpi=" + dpi + " and datediff(CURRENT_DATE , plan_time) between -3 and 0  and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
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

    final_dict = {"data": list}
    conn.close()
    return json.dumps(final_dict)
# 已完成
@yuelai.route('/event/table/complete',methods=["POST"]) #dpi,page
def complete():

    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()


    if dpi=="0":

        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id where finish_time is not null LIMIT " + str((page-1)*10) + ',10'
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

        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id where yuelai_event.dpi=" + dpi + " and finish_time is not null LIMIT " + str((page - 1) * 10) + ',10'
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

    final_dict = {"data": list}
    conn.close()
    return json.dumps(final_dict)
# 计划内
@yuelai.route('/event/table/in_plan',methods=["POST"]) #dpi,page
def in_plan():

    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    if dpi=="0":

        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id where datediff(CURRENT_DATE , plan_time)<-3  and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
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
        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id where yuelai_event.dpi=" + dpi + " and datediff(CURRENT_DATE , plan_time)<-3  and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
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

    final_dict = {"data": list}
    conn.close()
    return json.dumps(final_dict)
# 总数获取
@yuelai.route('/event/table/count')
def count():
    #数据库查询语句(通用)
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    complete_data = 'SELECT yuelai_event.id from yuelai_event where finish_time is not null '
    in_plan_data = "SELECT yuelai_event.id from yuelai_event where datediff(CURRENT_DATE , plan_time)<-3 and finish_time is null"
    near_data = "SELECT yuelai_event.id from yuelai_event where datediff(CURRENT_DATE , plan_time) between -3 and 0 and finish_time is null"
    late_data = "SELECT yuelai_event.id from yuelai_event where datediff(CURRENT_DATE , plan_time)>0 and finish_time is null"

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
    final_dict = {"data":count_dict}
    conn.close()
    return json.dumps(final_dict)
# 页数
@yuelai.route('/event/table/page',methods=['POST']) #dpi
def page():
    data = request.get_json()
    dpi = data["dpi"]
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='shenzhen_event',
                                   auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    if dpi == "0":

        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id"

        cursor.execute(table)

        result = cursor.fetchall()

        list_late = []
        list_complete = []
        list_near = []
        list_in_plan = []

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

            if state == 999999:
                list_complete.append(dict)

            if state>0 and state <999999:
                list_late.append(dict)

            if state<1 and state>-4:
                list_near.append(dict)

            if state<-3:
                list_in_plan.append((dict))

            count_dict = {"total":len(list_late)+len(list_near)+len(list_in_plan)+len(list_complete),"late":len(list_late),"near":len(list_near),"in_plan":len(list_in_plan),"complete":len(list_complete)}

            count_list =[]

            count_list.append(count_dict)

    else:
        table = "SELECT yuelai_event.id,event_name, start_plan ,plan_time, finish_time, department,name from yuelai_event JOIN yuelai_person ON yuelai_event.dpi=yuelai_person.id where yuelai_event.dpi=" + dpi

        cursor.execute(table)

        result = cursor.fetchall()

        list_late = []
        list_complete = []
        list_near = []
        list_in_plan = []

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
                    'finish_time': finish_time, 'state': state,
                    'department': department, "contector": contector}

            if state == 999999:
                list_complete.append(dict)

            if state > 0 and state < 999999:
                list_late.append(dict)

            if state < 1 and state > -4:
                list_near.append(dict)

            if state < -3:
                list_in_plan.append((dict))

            count_dict = {"total":len(list_late)+len(list_near)+len(list_in_plan)+len(list_complete),"late":len(list_late),"near":len(list_near),"in_plan":len(list_in_plan),"complete":len(list_complete)}

            count_list = []

            count_list.append(count_dict)

    dict = {"data":count_dict}
    conn.close()
    return json.dumps(dict)


# 部门接口
@yuelai.route('/event/table/company')
def yuelai_event_company():
    dict = {"data":[{"dpi":"1","name":"总包(钟晓旭)","person":"钟晓旭"},{"dpi":"2","name":"总包(江桃)","person":"江桃"},{"dpi":"3","name":"总包(赵瑞凡)","person":"赵瑞凡"},{"dpi":"4","name":"总包(达德文)","person":"达德文"}]}
    return json.dumps(dict)

# 监控页面
@yuelai.route("/cam")
def yuelai_cam():
    namelist = []
    urllist = []
    url = []

    list = [{u'installName':u"施工大门",
             u'coverUrl': u'http://120.79.164.6:18007/cover/f867433bdfb24797aebdb857270e0fd4.jpg', u'videoId': u'3604',
             u'getPlayUrl': u'http://47.112.142.114:18008/api/video/get-video-play-url-for-external?cameraNo='},
            {u'installName': u'员工通道',
             u'coverUrl': u'http://120.79.164.6:18007/cover/a64d3bcc55264568b55a6483c3468857.jpg', u'videoId': u'3605',
             u'getPlayUrl': u'http://47.112.142.114:18008/api/video/get-video-play-url-for-external?cameraNo='},
            {u'installName': u'大门内',
             u'coverUrl': u'http://120.79.164.6:18007/cover/f53f02e0ec12493189353eab41270173.jpg', u'videoId': u'3606',
             u'getPlayUrl': u'http://47.112.142.114:18008/api/video/get-video-play-url-for-external?cameraNo='},
            {u'installName': u'施工现场一',
             u'coverUrl': u'http://120.79.164.6:18007/cover/7303b4b6feff4bf69d52375351477758.jpg', u'videoId': u'3607',
             u'getPlayUrl': u'http://47.112.142.114:18008/api/video/get-video-play-url-for-external?cameraNo='},
            {u'installName': u'施工现场二',
             u'coverUrl': u'http://120.79.164.6:18007/cover/5863698cf0db49f59518e727bfffdd5d.jpg', u'videoId': u'3608',
             u'getPlayUrl': u'http://47.112.142.114:18008/api/video/get-video-play-url-for-external?cameraNo='},
            {u'installName': u'施工现场三',
             u'coverUrl': u'http://120.79.164.6:18007/cover/d2cb4e8c8ac64d8790d843f015a42c92.jpg', u'videoId': u'3609',
             u'getPlayUrl': u'http://47.112.142.114:18008/api/video/get-video-play-url-for-external?cameraNo='},
            {u'installName': u'项目部大门',
             u'coverUrl': u'http://120.79.164.6:18007/cover/2322134acafc4dd68419c5eb65353bb5.jpg', u'videoId': u'3610',
             u'getPlayUrl': u'http://47.112.142.114:18008/api/video/get-video-play-url-for-external?cameraNo='},
            {u'installName': u'施工现场四',
             u'coverUrl': u'http://120.79.164.6:18007/cover/fbd20387d729450d847ab29fb66d76ba.jpg', u'videoId': u'3611',
             u'getPlayUrl': u'http://47.112.142.114:18008/api/video/get-video-play-url-for-external?cameraNo='},
            {u'installName': u'施工现场五',
             u'coverUrl': u'http://120.79.164.6:18007/cover/78852868f887409e9664b180b9585dca.jpg', u'videoId': u'3826',
             u'getPlayUrl': u'http://47.112.142.114:18008/api/video/get-video-play-url-for-external?cameraNo='},
            {u'installName': u'项目部后门',
             u'coverUrl': u'http://120.79.164.6:18007/cover/d90c0a87be3d40e48ca24cde8c0be9c7.jpg', u'videoId': u'3827',
             u'getPlayUrl': u'http://47.112.142.114:18008/api/video/get-video-play-url-for-external?cameraNo='}]
    for i in list:
        namelist.append(i["installName"])
        urllist.append(str(i["getPlayUrl"]) + str(i["videoId"]))
    # print namelist
    # print urllist

    for j in urllist:
        data = requests.get(j)
        data = json.loads(data.content)
        data = data["data"]["playUrl"]
        url.append(data)

    finallist=[]
    for k in range(10):
        dict = {"name":namelist[k],"url":url[k]}
        finallist.append(dict)

    final = {"data":finallist}

    return json.dumps(final)



# 人员
@yuelai.route('/data_person',methods=['POST'])
def data_person():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='yuelai_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    data = request.get_json()
    personName = data["personName"]
    positionName = data["positionName"]
    inOut = int(data["inOut"])
    companyName = data["companyName"]
    pictureUrl = data["pictureUrl"]
    accessTime = data["time"]


    sql = "insert into access (personName,positionName,inOrout,companyName,pictureUrl,accessTime) values(%s,%s,%d,%s,%s,%s)"%("'"+personName+"'","'"+positionName+"'",inOut,"'"+companyName+"'","'"+pictureUrl+"'","'"+accessTime+"'")
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return "已收到数据"



# 环境
@yuelai.route('/data_environment',methods=['POST'])
def data_environment():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='yuelai_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    data = request.get_json()
    deviceSerial = data["deviceSerial"]
    recordtime = data["recordTime"]
    temperature = float(data["temperature"])
    humidity = float(data["humidity"])
    pm2p5 = float(data["pm2p5"])
    pm10 = float(data["pm10"])
    noise = float(data["noise"])
    windspeed = float(data["windSpeed"])
    winddirection = float(data["windDirection"])


    sql = "insert into environment (deviceSerial,recordtime,temperature,humidity,pm2p5,pm10,noise,windspeed,winddirection) values(%s,%s,%f,%f,%f,%f,%f,%f,%f)"%("'"+deviceSerial+"'","'"+recordtime+"'",temperature,humidity,pm2p5,pm10,noise,windspeed,winddirection)
    cursor.execute(sql)
    conn.commit()
    conn.close()

    return "已收到数据"


# 人员管理接口
# 管理人员
@yuelai.route("/renyuan/guanli")
def guanli():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='yuelai_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_laowu = """
                    SELECT
    	personName,
    	positionName,

    IF (inOrout = 0, '进场', '出场') AS entry,
     DATE_FORMAT(
    	accessTime,
    	'%Y-%m-%d %H:%i:%s'
    ) AS accessTime,
     companyName
    FROM
    	access
    WHERE
    DATE_FORMAT(accessTime, '%Y-%m-%d') = date_format(CURRENT_DATE, '%Y-%m-%d')
    AND positionName NOT IN (
    '砌筑工',
    '建筑瓦工',
    '瓦工',
    '窑炉修筑工',
    '钢筋工',
    '架子工',
    '普通架子工',
    '附着升降脚手架安装拆卸工',
    '高处作业吊篮操作工',
    '高处作业吊篮安装拆卸工',
    '混凝土工',
    '模板工',
    '混凝土模板工',
    '机械设备安装工',
    '通风工',
    '起重工',
    '安装起重工',
    '安装钳工',
    '电气设备安装工',
    '电气安装调试工',
    '管工',
    '管道工',
    '变电安装工',
    '电工',
    '弱电工',
    '司泵工',
    '挖掘铲运和桩工机械司机',
    '推土机司机',
    '铲运机司机',
    '土石方挖掘机司机',
    '打桩工',
    '桩机操作工',
    '起重信号工',
    '起重信号司索工',
    '建筑起重机械安装拆卸工',
    '装饰装修工',
    '抹灰工',
    '油漆工',
    '镶贴工',
    '涂裱工',
    '装饰装修木工',
    '室内成套设施安装工',
    '建筑门窗幕墙安装工',
    '慕墙安装工',
    '建筑门窗安装工',
    '幕墙制作工',
    '防水工',
    '木工',
    '手工木工',
    '精细木工',
    '石工',
    '石作业工',
    '焊工',
    '电焊工',
    '爆破工',
    '除尘工',
    '测量放线工',
    '测量工',
    '线路架设工',
    '古建筑传统木工',
    '木雕工',
    '愿额工',
    '古建筑传统瓦工',
    '砧刻工',
    '砌花街工',
    '泥塑工',
    '古建筑传统石工',
    '石雕工',
    '砧细工',
    '古建筑传统彩画工',
    '彩绘工',
    '古建筑传统油工',
    '推光漆工',
    '泥工',
    '玻璃工',
    '吊车司机与指挥',
    '机修工',
    '维修电工',
    '水工',
    '杂工'
    )
        """
    cursor.execute(sql_laowu)
    guanli = cursor.fetchall()
    list = []
    for i in guanli:
        dict = {
            "name": i[0],
            "type": i[1],
            "state": i[2],
            "time": i[3],
            "company": i[4]
        }
        list.append(dict)

    conn.close()
    return json.dumps(list)


# 劳务人员
@yuelai.route("/renyuan/laowu")
def laowu():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='yuelai_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_laowu = """
                SELECT
	personName,
	positionName,

IF (inOrout = 0, '进场', '出场') AS entry,
 DATE_FORMAT(
	accessTime,
	'%Y-%m-%d %H:%i:%s'
) AS accessTime,
 companyName
FROM
	access
WHERE
DATE_FORMAT(accessTime, '%Y-%m-%d') = date_format(CURRENT_DATE, '%Y-%m-%d')
AND positionName IN (
'砌筑工',
'建筑瓦工',
'瓦工',
'窑炉修筑工',
'钢筋工',
'架子工',
'普通架子工',
'附着升降脚手架安装拆卸工',
'高处作业吊篮操作工',
'高处作业吊篮安装拆卸工',
'混凝土工',
'模板工',
'混凝土模板工',
'机械设备安装工',
'通风工',
'起重工',
'安装起重工',
'安装钳工',
'电气设备安装工',
'电气安装调试工',
'管工',
'管道工',
'变电安装工',
'电工',
'弱电工',
'司泵工',
'挖掘铲运和桩工机械司机',
'推土机司机',
'铲运机司机',
'土石方挖掘机司机',
'打桩工',
'桩机操作工',
'起重信号工',
'起重信号司索工',
'建筑起重机械安装拆卸工',
'装饰装修工',
'抹灰工',
'油漆工',
'镶贴工',
'涂裱工',
'装饰装修木工',
'室内成套设施安装工',
'建筑门窗幕墙安装工',
'慕墙安装工',
'建筑门窗安装工',
'幕墙制作工',
'防水工',
'木工',
'手工木工',
'精细木工',
'石工',
'石作业工',
'焊工',
'电焊工',
'爆破工',
'除尘工',
'测量放线工',
'测量工',
'线路架设工',
'古建筑传统木工',
'木雕工',
'愿额工',
'古建筑传统瓦工',
'砧刻工',
'砌花街工',
'泥塑工',
'古建筑传统石工',
'石雕工',
'砧细工',
'古建筑传统彩画工',
'彩绘工',
'古建筑传统油工',
'推光漆工',
'泥工',
'玻璃工',
'吊车司机与指挥',
'机修工',
'维修电工',
'水工',
'杂工'
)

    """
    cursor.execute(sql_laowu)
    guanli = cursor.fetchall()
    list = []
    for i in guanli:
        dict = {
            "name": i[0],
            "type":i[1],
            "state": i[2],
            "time": i[3],
            "company": i[4]
        }
        list.append(dict)

    conn.close()
    return json.dumps(list)


# 专业分包
@yuelai.route("/renyuan/zhuanyefenbao")
def zhuanyefenbao():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='yuelai_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_laowu = """
                    SELECT
    	personName,
    	positionName,

    IF (inOrout = 0, '进场', '出场') AS entry,
     DATE_FORMAT(
    	accessTime,
    	'%Y-%m-%d %H:%i:%s'
    ) AS accessTime,
     companyName
    FROM
    	access
    WHERE
    DATE_FORMAT(accessTime, '%Y-%m-%d') = date_format(CURRENT_DATE, '%Y-%m-%d')
    AND positionName NOT IN (
    '砌筑工',
    '建筑瓦工',
    '瓦工',
    '窑炉修筑工',
    '钢筋工',
    '架子工',
    '普通架子工',
    '附着升降脚手架安装拆卸工',
    '高处作业吊篮操作工',
    '高处作业吊篮安装拆卸工',
    '混凝土工',
    '模板工',
    '混凝土模板工',
    '机械设备安装工',
    '通风工',
    '起重工',
    '安装起重工',
    '安装钳工',
    '电气设备安装工',
    '电气安装调试工',
    '管工',
    '管道工',
    '变电安装工',
    '电工',
    '弱电工',
    '司泵工',
    '挖掘铲运和桩工机械司机',
    '推土机司机',
    '铲运机司机',
    '土石方挖掘机司机',
    '打桩工',
    '桩机操作工',
    '起重信号工',
    '起重信号司索工',
    '建筑起重机械安装拆卸工',
    '装饰装修工',
    '抹灰工',
    '油漆工',
    '镶贴工',
    '涂裱工',
    '装饰装修木工',
    '室内成套设施安装工',
    '建筑门窗幕墙安装工',
    '慕墙安装工',
    '建筑门窗安装工',
    '幕墙制作工',
    '防水工',
    '木工',
    '手工木工',
    '精细木工',
    '石工',
    '石作业工',
    '焊工',
    '电焊工',
    '爆破工',
    '除尘工',
    '测量放线工',
    '测量工',
    '线路架设工',
    '古建筑传统木工',
    '木雕工',
    '愿额工',
    '古建筑传统瓦工',
    '砧刻工',
    '砌花街工',
    '泥塑工',
    '古建筑传统石工',
    '石雕工',
    '砧细工',
    '古建筑传统彩画工',
    '彩绘工',
    '古建筑传统油工',
    '推光漆工',
    '泥工',
    '玻璃工',
    '吊车司机与指挥',
    '机修工',
    '维修电工',
    '水工',
    '杂工'
    )
    AND 
    companyName NOT IN ('中国建筑第八工程局有限公司')
        """
    cursor.execute(sql_laowu)
    guanli = cursor.fetchall()
    list = []
    for i in guanli:
        dict = {
            "name": i[0],
            "type": i[1],
            "state": i[2],
            "time": i[3],
            "company": i[4]
        }
        list.append(dict)

    conn.close()
    return json.dumps(list)


# 人员统计
@yuelai.route("/renyuan/renyuantongji")
def renyuantongji():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='yuelai_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_renyuantongji = """
SELECT
	count(*) AS y,
	DATE_FORMAT(accessTime, '%m-%d') AS x,
	CASE

WHEN companyName = "中国建筑第八工程局有限公司" THEN
	1
WHEN companyName = "东北院" THEN
	2
END s
FROM
	(
		SELECT
			personName,
			companyName,
			DATE_FORMAT(accessTime, '%Y-%m-%d') AS accessTime
		FROM
			access
		WHERE
			DATE_FORMAT(accessTime, '%Y-%m-%d') BETWEEN DATE_SUB(CURRENT_DATE, INTERVAL 6 DAY)
		AND DATE_FORMAT(CURRENT_DATE, '%Y-%m-%d')
		AND inOrout = 0
		GROUP BY
			1,
			2,
			3
	) AS a
GROUP BY
	s,
	x
ORDER BY
	s"""

    cursor.execute(sql_renyuantongji)
    renyuantongji = cursor.fetchall()

    dict_1 = {}
    dict_2 = {}
    # dict_3 = {}
    # dict_4 = {}
    # dict_5 = {}
    # dict_6 = {}
    for i in renyuantongji:
        if i[2] == 1:
            dict_1[i[1]] = i[0]
            # dict_3[i[1]] = 0
            dict_2[i[1]] = 0
            # dict_4[i[1]] = 0
            # dict_5[i[1]] = 0
            # dict_6[i[1]] = 0
        # if i[2] == 3:
        #     dict_3[i[1]] = i[0]
        if i[2] == 2:
            dict_2[i[1]] = i[0]
        # if i[2] == 4:
        #     dict_4[i[1]] = i[0]
        # if i[2] == 5:
        #     dict_5[i[1]] = i[0]
        # if i[2] == 6:
        #     dict_6[i[1]] = i[0]

    list_x = []
    for j in sorted(dict_1):
        list_x.append(j)

    list_1 = []
    list_2 = []
    # list_3 = []
    # list_4 = []
    # list_5 = []
    # list_6 = []
    for k_1 in sorted(dict_1):
        list_1.append(dict_1[k_1])
    for k_2 in sorted(dict_2):
        list_2.append(dict_2[k_2])
    # for k_3 in sorted(dict_3):
    #     list_3.append(dict_3[k_3])
    # for k_4 in sorted(dict_4):
    #     list_4.append(dict_4[k_4])
    # for k_5 in sorted(dict_5):
    #     list_5.append(dict_5[k_5])
    # for k_6 in sorted(dict_6):
    #     list_6.append(dict_6[k_6])

    dict = {
        "x": list_x,
        "y": [{"name": "东北院", "data": list_2},
              {"name": "中国建筑第八工程局有限公司", "data": list_1}]

    }

    conn.close()

    return json.dumps(dict)

def takeSecond(elem):
    return elem

# 工种统计
@yuelai.route("/renyuan/gongzhong")
def gongzhong():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='yuelai_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql = """
            select distinct positionName from access where DATE_FORMAT(accessTime, '%Y-%m-%d')= DATE_FORMAT(CURRENT_DATE, '%Y-%m-%d') AND inOrout = 0  AND positionName IN (
'砌筑工',
'建筑瓦工',
'瓦工',
'窑炉修筑工',
'钢筋工',
'架子工',
'普通架子工',
'附着升降脚手架安装拆卸工',
'高处作业吊篮操作工',
'高处作业吊篮安装拆卸工',
'混凝土工',
'模板工',
'混凝土模板工',
'机械设备安装工',
'通风工',
'起重工',
'安装起重工',
'安装钳工',
'电气设备安装工',
'电气安装调试工',
'管工',
'管道工',
'变电安装工',
'电工',
'弱电工',
'司泵工',
'挖掘铲运和桩工机械司机',
'推土机司机',
'铲运机司机',
'土石方挖掘机司机',
'打桩工',
'桩机操作工',
'起重信号工',
'起重信号司索工',
'建筑起重机械安装拆卸工',
'装饰装修工',
'抹灰工',
'油漆工',
'镶贴工',
'涂裱工',
'装饰装修木工',
'室内成套设施安装工',
'建筑门窗幕墙安装工',
'慕墙安装工',
'建筑门窗安装工',
'幕墙制作工',
'防水工',
'木工',
'手工木工',
'精细木工',
'石工',
'石作业工',
'焊工',
'电焊工',
'爆破工',
'除尘工',
'测量放线工',
'测量工',
'线路架设工',
'古建筑传统木工',
'木雕工',
'愿额工',
'古建筑传统瓦工',
'砧刻工',
'砌花街工',
'泥塑工',
'古建筑传统石工',
'石雕工',
'砧细工',
'古建筑传统彩画工',
'彩绘工',
'古建筑传统油工',
'推光漆工',
'泥工',
'玻璃工',
'吊车司机与指挥',
'机修工',
'维修电工',
'水工',
'杂工'
)
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    x=[]
    list_y=[]
    for i in result:
        x.append(i[0])
    for j in x:
        sql = "select count(DISTINCT personName) from access where DATE_FORMAT(accessTime, '%Y-%m-%d')= DATE_FORMAT(CURRENT_DATE, '%Y-%m-%d') AND positionName = '"+str(j)+"' AND inOrout = 0"
        cursor.execute(sql)
        result = cursor.fetchone()
        list_y.append(int(result[0]))
    list_final=[]
    for k in range(len(x)):
        dict = {"x":x[k],
                "y":list_y[k]}
        list_final.append(dict)
    list_final.sort(key=lambda k: (k.get('y', 0)))

    list_xxx=[]
    list_yyy=[]
    for m in list_final:
        list_xxx.append(m["x"])
        list_yyy.append(m["y"])

    dict_final = {"x":list_xxx,
                  "y":{"data":list_yyy}}
    return json.dumps(dict_final)
