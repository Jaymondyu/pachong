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

jiangjin = Blueprint('jiangjin', __name__ ,static_folder="../static")


# 江津滨江新城大屏
# @jiangjin.route("/")
# def index():
#     return render_template("jiangjin_index.html")


@jiangjin.route("/insert")
def jiangjin_insert():
    return render_template("jiangjin_insert.html")


# 江津驾驶舱接口
# 天气
@jiangjin.route("/index/weather")
def index_weather():
    # 数据库查询
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_weather = "select pm2p5,pm10,noise,temperature from environment order by id desc LIMIT 1"
    cursor.execute(sql_weather)
    enviroment = cursor.fetchall()
    # 获取剩余天数
    days = requests.get("http://183.66.213.82:8888/shenzhen/date/begin?d=2019-02-19")
    days = days.text
    days = int(days[10:-2])
    # 整合
    list = {
        "pm2p5": enviroment[0][0],
        "pm10": enviroment[0][1],
        "noise": enviroment[0][2],
        "temperature": enviroment[0][3],
        "days": days
    }
    conn.close()
    return json.dumps(list)


# 人员统计
@jiangjin.route("/index/renyuan")
def index_renyuan():
    # 数据库查询
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_renyuan = """
                    SELECT
                        count(*) AS y,
                        DATE_FORMAT(attendancetime, '%m-%d') AS x,
                    case 
                    when department in ("重庆建工住宅建设有限公司","林同棪【重庆】国际工程技术有限公司")then 1 
                    when department in  ("重庆正旋基础有限公司","重庆名庆防水工程有限公司","重庆力杰消防工程有限公司" )then 3
                    when department = "重庆联文建筑劳务有限公司" then 2
                    end s
                    FROM
                        (select access.name,department_person.department, DATE_FORMAT(attendancetime, '%Y-%m-%d') as attendancetime from access,department_person
                    WHERE
                        access.name=department_person.name
	                    and
                        DATE_FORMAT(attendancetime, '%Y-%m-%d') BETWEEN DATE_SUB(CURRENT_DATE, INTERVAL 6 DAY) AND DATE_FORMAT(CURRENT_DATE, '%Y-%m-%d')
                    AND entry = 1
                    group by 1,2,3

                    ) as a
                    GROUP BY s,x
                    ORDER BY s
                """
    cursor.execute(sql_renyuan)
    renyuan = cursor.fetchall()
    dict_1 = {}
    dict_2 = {}
    dict_3 = {}
    for i in renyuan:
        if i[2] == 1:
            dict_1[i[1]] = i[0]
            dict_3[i[1]] = 0
            dict_2[i[1]] = 0

        if i[2] == 3:
            dict_3[i[1]] = i[0]
        if i[2] == 2:
            dict_2[i[1]] = i[0]

    list_x = []
    for j in sorted(dict_1):
        list_x.append(j)

    list_1 = []
    list_2 = []
    list_3 = []

    for k_1 in sorted(dict_1):
        list_1.append(dict_1[k_1])
    for k_2 in sorted(dict_2):
        list_2.append(dict_2[k_2])
    for k_3 in sorted(dict_3):
        list_3.append(dict_3[k_3])

    dict = {
        "x": list_x,
        "y": [{"name": "管理人员", "data": list_1}, {"name": "劳务人员", "data": list_2}, {"name": "专业分包", "data": list_3}]

    }
    conn.close()
    return json.dumps(dict)


# 安全问题
@jiangjin.route("/index/anquan")
def index_safe():
    # 日期确认
    datetime_now = datetime.datetime.now()
    this_month = datetime.datetime.now().strftime('%Y-%m')
    last_1_month = (datetime_now - relativedelta(months=1)).strftime('%Y-%m')
    last_2_month = (datetime_now - relativedelta(months=2)).strftime('%Y-%m')
    last_3_month = (datetime_now - relativedelta(months=3)).strftime('%Y-%m')
    last_4_month = (datetime_now - relativedelta(months=4)).strftime('%Y-%m')
    month_now = []
    month_1_before = []
    month_2_before = []
    month_3_before = []
    month_4_before = []
    month_long = []
    # 安全部分

    url_1 = "http://www.tylinbim.com/wui/safeProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]
    for i in dataList_1:
        if str(i["checkTime"][0:7]) == this_month:
            month_now.append(i)
        elif str(i["checkTime"][0:7]) == last_1_month:
            month_1_before.append(i)
        elif str(i["checkTime"][0:7]) == last_2_month:
            month_2_before.append(i)
        elif str(i["checkTime"][0:7]) == last_3_month:
            month_3_before.append(i)
        elif str(i["checkTime"][0:7]) == last_4_month:
            month_4_before.append(i)
        else:
            pass

    for nnd in dataList_1:
        if str(nnd["checkTime"][0:7]) != last_4_month:
            if int(str(datetime.datetime.strptime(str(nnd["checkTime"][0:7]), '%Y-%m') - datetime.datetime.strptime(
                    last_4_month, '%Y-%m')).replace(" days, 0:00:00", "")) < 0:
                month_long.append(nnd)

    month_now_solved = []
    month_1_before_solved = []
    month_2_before_solved = []
    month_3_before_solved = []
    month_4_before_solved = []
    for j in month_now:
        if j["rectificate"] == "是":
            month_now_solved.append(j)
    for k in month_1_before:
        if k["rectificate"] == "是":
            month_1_before_solved.append(k)
    for l in month_2_before:
        if l["rectificate"] == "是":
            month_2_before_solved.append(l)
    for m in month_3_before:
        if m["rectificate"] == "是":
            month_3_before_solved.append(m)
    for n in month_4_before:
        if n["rectificate"] == "是":
            month_4_before_solved.append(n)

    y = {
        "total": [len(month_4_before), len(month_3_before), len(month_2_before), len(month_1_before), len(month_now)],
        "solved": [len(month_4_before_solved), len(month_3_before_solved), len(month_2_before_solved),
                   len(month_1_before_solved), len(month_now_solved)],
        "ALL": [len(month_long) + len(month_4_before), len(month_long) + len(month_4_before) + len(month_3_before),
                len(month_long) + len(month_4_before) + len(month_3_before) + len(month_2_before),
                len(month_long) + len(month_4_before) + len(month_3_before) + len(month_2_before) + len(month_1_before),
                len(month_long) + len(month_4_before) + len(month_3_before) + len(month_2_before) + len(
                    month_1_before) + len(month_now)]
    }
    x = [last_4_month, last_3_month, last_2_month, last_1_month, this_month]

    dict = {"y": y, "x": x}

    return json.dumps(dict)


# 质量问题
@jiangjin.route("/index/zhiliang")
def index_quality():
    # 日期确认
    datetime_now = datetime.datetime.now()
    this_month = datetime.datetime.now().strftime('%Y-%m')
    last_1_month = (datetime_now - relativedelta(months=1)).strftime('%Y-%m')
    last_2_month = (datetime_now - relativedelta(months=2)).strftime('%Y-%m')
    last_3_month = (datetime_now - relativedelta(months=3)).strftime('%Y-%m')
    last_4_month = (datetime_now - relativedelta(months=4)).strftime('%Y-%m')
    month_now = []
    month_1_before = []
    month_2_before = []
    month_3_before = []
    month_4_before = []
    month_long = []
    # 安全部分

    url_1 = "http://www.tylinbim.com/wui/qualityProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]
    for i in dataList_1:
        if str(i["checkTime"][0:7]) == this_month:
            month_now.append(i)
        elif str(i["checkTime"][0:7]) == last_1_month:
            month_1_before.append(i)
        elif str(i["checkTime"][0:7]) == last_2_month:
            month_2_before.append(i)
        elif str(i["checkTime"][0:7]) == last_3_month:
            month_3_before.append(i)
        elif str(i["checkTime"][0:7]) == last_4_month:
            month_4_before.append(i)
        else:
            pass

    for nnd in dataList_1:
        if str(nnd["checkTime"][0:7]) != last_4_month:
            if int(str(datetime.datetime.strptime(str(nnd["checkTime"][0:7]), '%Y-%m') - datetime.datetime.strptime(
                    last_4_month, '%Y-%m')).replace(" days, 0:00:00", "")) < 0:
                month_long.append(nnd)

    month_now_solved = []
    month_1_before_solved = []
    month_2_before_solved = []
    month_3_before_solved = []
    month_4_before_solved = []
    for j in month_now:
        if j["rectificate"] == "是":
            month_now_solved.append(j)
    for k in month_1_before:
        if k["rectificate"] == "是":
            month_1_before_solved.append(k)
    for l in month_2_before:
        if l["rectificate"] == "是":
            month_2_before_solved.append(l)
    for m in month_3_before:
        if m["rectificate"] == "是":
            month_3_before_solved.append(m)
    for n in month_4_before:
        if n["rectificate"] == "是":
            month_4_before_solved.append(n)

    y = {
        "total": [len(month_4_before), len(month_3_before), len(month_2_before), len(month_1_before), len(month_now)],
        "solved": [len(month_4_before_solved), len(month_3_before_solved), len(month_2_before_solved),
                   len(month_1_before_solved), len(month_now_solved)],
        "ALL": [len(month_long) + len(month_4_before), len(month_long) + len(month_4_before) + len(month_3_before),
                len(month_long) + len(month_4_before) + len(month_3_before) + len(month_2_before),
                len(month_long) + len(month_4_before) + len(month_3_before) + len(month_2_before) + len(month_1_before),
                len(month_long) + len(month_4_before) + len(month_3_before) + len(month_2_before) + len(
                    month_1_before) + len(month_now)]
    }
    x = [last_4_month, last_3_month, last_2_month, last_1_month, this_month]

    dict = {"y": y, "x": x}

    return json.dumps(dict)


# 进度
@jiangjin.route("/index/jindu")
def jindu():
    now_date = datetime.datetime.today().strftime('%Y-%m-%d')
    urn = "http://183.66.213.82:8888/processandprice_jiangjin/getprocessandprice_jiangjin?time=" + now_date
    result = (requests.get(urn)).content
    result = json.loads(result)
    jiegou = float(result["price_finish"]) / float(result["price_inall"])
    jiegou = int(jiegou * 100)

    list = [
        {"data": jiegou,
         "name": "结构工程"},
        {"data": 3.39,
         "name": "建筑工程"},
        {"data": 0,
         "name": "机电工程"},
        {"data": 0,
         "name": "幕墙工程"},
        {"data": 0,
         "name": "精装工程"},
        {"data": 0,
         "name": "景观工程"}
    ]
    return json.dumps(list)


# 项目概况
@jiangjin.route("/index/intro")
def intro():
    dict = {
        "data": "本项目位于重庆市江津区滨江新城核心区A7-07-2/01地块，新建项目用地北侧及西侧紧邻城市道路，交通便捷，东侧与未建居住用地相临，南侧与公园绿地相临并有城市高压线。本项目总建筑面积91342.37m2，其中地上面积67040.15m2，地下面积24302.22 m2。地上建筑主要由行政办公、商务办公A栋及其裙房行政服务中心、商务办公B栋组成，地下部分主要为地下车库及设备用房。行政办公、商务办公均为二类高层公共建筑，属二类办公建筑，行政服务中心为高层建筑裙房，耐火等级均为一级，地下车库为I类停车库，耐火等级为一级,本工程地势为南高北低，标高在256.7~269.0米之间；高差约13米，结构主体采用框架结构体系。"}
    return json.dumps(dict)


# 参建单位
@jiangjin.route("/index/company")
def company():
    list = [
        {
            "unit": "建设单位",
            "company": "重庆市江津区滨江新城开发建设集团有限公司"
        },
        {
            "unit": "勘察单位",
            "company": "重庆市设计院"
        }, {
            "unit": "设计单位",
            "company": "重庆市设计院"
        }, {
            "unit": "施工总包单位",
            "company": "重庆建工住宅建设有限公司"
        }, {
            "unit": "BIM咨询及监理单位",
            "company": "林同棪（重庆）国际工程技术有限公司"
        }
    ]
    return json.dumps(list)


# 人员管理接口
# 管理人员
@jiangjin.route("/renyuan/guanli")
def guanli():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_guanli = """SELECT 
            access.name, personnel.role, personnel.telephone, if(entry=1,'进场','出场') as entry, DATE_FORMAT(attendancetime,'%Y-%m-%d %H:%i:%s') as attendancetime, department_person.department 
            from access,personnel,department_person 
            where access.name=personnel.name
            and access.name=department_person.name
            and 
            DATE_FORMAT(attendancetime,'%Y-%m-%d') = date_format(CURRENT_DATE,'%Y-%m-%d') 
            AND
             department_person.department in ('重庆建工住宅建设有限公司','林同棪【重庆】国际工程技术有限公司')"""

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

    conn.close()
    return json.dumps(list)


# 劳务人员
@jiangjin.route("/renyuan/laowu")
def laowu():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_laowu = """
                SELECT 
                access.name, department_person.department,if(entry=1,'进场','出场') as entry, DATE_FORMAT(attendancetime,'%Y-%m-%d %H:%i:%s') as attendancetime 
                from access,department_person 
                where
								access.name=department_person.name
								and
                DATE_FORMAT(attendancetime,'%Y-%m-%d') = date_format(CURRENT_DATE,'%Y-%m-%d') 
                AND 
                department_person.department in ('重庆联文建筑劳务有限公司')
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

    conn.close()
    return json.dumps(list)


# 专业分包
@jiangjin.route("/renyuan/zhuanyefenbao")
def zhuanyefenbao():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_zhuanyefenbao = """
            SELECT access.name, department_person.department,if(entry=1,'进场','出场') as entry, DATE_FORMAT(attendancetime,'%Y-%m-%d %H:%i:%s') as attendancetime 
            from access,department_person  
            where 
						access.name=department_person.name
						and
						DATE_FORMAT(attendancetime,'%Y-%m-%d') = date_format(CURRENT_DATE,'%Y-%m-%d') 
            AND department_person.department in ('重庆正旋基础有限公司','重庆名庆防水工程有限公司','重庆力杰消防工程有限公司')

    """
    cursor.execute(sql_zhuanyefenbao)
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

    conn.close()
    return json.dumps(list)


# 人员统计
@jiangjin.route("/renyuan/renyuantongji")
def renyuantongji():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_renyuantongji = """
  SELECT
	count(*) AS y,
	DATE_FORMAT(attendancetime, '%m-%d') AS x,
	CASE
WHEN department = "重庆建工住宅建设有限公司" THEN
	3
WHEN department = "重庆正旋基础有限公司" THEN
	2
WHEN department = "重庆联文建筑劳务有限公司" THEN
	1
WHEN department = "林同棪【重庆】国际工程技术有限公司" THEN
	4
WHEN department = "重庆名庆防水工程有限公司" THEN
	5
WHEN department = "重庆力杰消防工程有限公司" THEN
	6
END s
FROM
	(select access.name,department_person.department, DATE_FORMAT(attendancetime, '%Y-%m-%d') as attendancetime from access,department_person
WHERE
	access.name=department_person.name
	and
	DATE_FORMAT(attendancetime, '%Y-%m-%d') BETWEEN DATE_SUB(CURRENT_DATE, INTERVAL 6 DAY) AND DATE_FORMAT(CURRENT_DATE, '%Y-%m-%d')
AND entry = 1
group by 1,2,3

) as a
GROUP BY s,x
ORDER BY s
    """

    cursor.execute(sql_renyuantongji)
    renyuantongji = cursor.fetchall()

    dict_1 = {}
    dict_2 = {}
    dict_3 = {}
    dict_4 = {}
    dict_5 = {}
    dict_6 = {}
    for i in renyuantongji:
        if i[2] == 1:
            dict_1[i[1]] = i[0]
            dict_3[i[1]] = 0
            dict_2[i[1]] = 0
            dict_4[i[1]] = 0
            dict_5[i[1]] = 0
            dict_6[i[1]] = 0
        if i[2] == 3:
            dict_3[i[1]] = i[0]
        if i[2] == 2:
            dict_2[i[1]] = i[0]
        if i[2] == 4:
            dict_4[i[1]] = i[0]
        if i[2] == 5:
            dict_5[i[1]] = i[0]
        if i[2] == 6:
            dict_6[i[1]] = i[0]

    list_x = []
    for j in sorted(dict_1):
        list_x.append(j)

    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
    for k_1 in sorted(dict_1):
        list_1.append(dict_1[k_1])
    for k_2 in sorted(dict_2):
        list_2.append(dict_2[k_2])
    for k_3 in sorted(dict_3):
        list_3.append(dict_3[k_3])
    for k_4 in sorted(dict_4):
        list_4.append(dict_4[k_4])
    for k_5 in sorted(dict_5):
        list_5.append(dict_5[k_5])
    for k_6 in sorted(dict_6):
        list_6.append(dict_6[k_6])

    dict = {
        "x": list_x,
        "y": [{"name": "重庆建工住宅建设有限公司", "data": list_3}, {"name": "重庆正旋基础有限公司", "data": list_2},
              {"name": "重庆联文建筑劳务有限公司", "data": list_1}, {"name": "林同棪【重庆】国际工程技术有限公司", "data": list_4},
              {"name": "重庆名庆防水工程有限公司", "data": list_5}, {"name": "重庆力杰消防工程有限公司", "data": list_6}]

    }

    conn.close()
    return json.dumps(dict)


# 环境监测接口
# 风速
# 圆环(当前)
@jiangjin.route("/environment/wind_now")
def wind_now():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_wind_now = """
            select windspeed as actual,10 as aims from environment order by recordtime desc LIMIT 1
    """

    cursor.execute(sql_wind_now)
    wind_now = cursor.fetchall()

    if wind_now[0][0] == None:
        wind_now_1 = 0
    else:
        wind_now_1 = wind_now[0][0]
    dict = {
        "wind_now": wind_now_1,
        "wind_total": wind_now[0][1],
        "data": (float(wind_now_1) / float(wind_now[0][1])) * 100
    }
    conn.close()
    return json.dumps(dict)


# 数字翻牌(今日最高)
@jiangjin.route("/environment/wind_high")
def wind_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_wind_high = """
            SELECT MAX(windspeed) as max_windspeed FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_wind_high)
    wind_high = cursor.fetchall()

    dict = {
        "data": wind_high[0][0]
    }
    conn.close()
    return json.dumps(dict)


# echart(全天)
@jiangjin.route("/environment/wind_echart")
def wind_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_wind_echart = """
            SELECT windspeed as y,DATE_FORMAT(recordtime,'%H:%i') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE order by x
    """

    cursor.execute(sql_wind_echart)
    wind_echart = cursor.fetchall()

    list_x = []
    list_data = []

    for i in wind_echart:
        list_data.append(i[0])
        list_x.append(i[1])

    for data in range(0, len(list_data)):
        if str(type(list_data[data])) == "<type 'NoneType'>":
            list_data[data] = 0.0

    dict = {
        "x": list_x,
        "y": {"data": list_data}
    }
    conn.close()
    return json.dumps(dict)


# 湿度
# 圆环(当前)
@jiangjin.route("/environment/humidity_now")
def humidity_now():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_humidity_now = """
            select humidity as actual,100 as aims from environment order by recordtime desc LIMIT 1
    """

    cursor.execute(sql_humidity_now)
    humidity_now = cursor.fetchall()

    dict = {
        "humidity_now": humidity_now[0][0],
        "humidity_total": humidity_now[0][1],
        "data": (float(humidity_now[0][0]) / float(humidity_now[0][1])) * 100
    }
    conn.close()
    return json.dumps(dict)


# 数字翻牌(今日最高)
@jiangjin.route("/environment/humidity_high")
def humidity_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_humidity_high = """
            SELECT MAX(humidity) as max_humidity FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_humidity_high)
    humidity_high = cursor.fetchall()

    dict = {
        "data": humidity_high[0][0]
    }
    conn.close()
    return json.dumps(dict)


# echart(全天)
@jiangjin.route("/environment/humidity_echart")
def humidity_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_humidity_echart = """
            SELECT humidity as y,DATE_FORMAT(recordtime,'%H:%i') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE order by x
    """

    cursor.execute(sql_humidity_echart)
    humidity_echart = cursor.fetchall()

    list_x = []
    list_data = []

    for i in humidity_echart:
        list_x.append(i[1])
        list_data.append(i[0])

    dict = {
        "x": list_x,
        "y": {"data": list_data}
    }
    conn.close()
    return json.dumps(dict)


# 温度
# 圆环(当前)
@jiangjin.route("/environment/temperature_now")
def temperature_now():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_temperature_now = """
            select temperature as actual,50 as aims from environment order by recordtime desc LIMIT 1
    """

    cursor.execute(sql_temperature_now)
    temperature_now = cursor.fetchall()

    dict = {
        "temperature_now": temperature_now[0][0],
        "temperature_total": temperature_now[0][1],
        "data": (float(temperature_now[0][0]) / float(temperature_now[0][1])) * 100
    }
    conn.close()
    return json.dumps(dict)


# 数字翻牌(今日最高)
@jiangjin.route("/environment/temperature_high")
def temperature_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_temperature_high = """
            SELECT MAX(temperature) as max_temperature FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_temperature_high)
    temperature_high = cursor.fetchall()

    dict = {
        "data": temperature_high[0][0]
    }
    conn.close()
    return json.dumps(dict)


# echart(全天)
@jiangjin.route("/environment/temperature_echart")
def temperature_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_temperature_echart = """
            SELECT temperature as y,DATE_FORMAT(recordtime,'%H:%i') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE order by x
    """

    cursor.execute(sql_temperature_echart)
    temperature_echart = cursor.fetchall()

    list_x = []
    list_data = []

    for i in temperature_echart:
        list_x.append(i[1])
        list_data.append(i[0])

    dict = {
        "x": list_x,
        "y": {"data": list_data}
    }
    conn.close()
    return json.dumps(dict)


# 噪音
# 圆环(当前)
@jiangjin.route("/environment/noise_now")
def noise_now():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_noise_now = """
            select noise as actual,140 as aims from environment order by recordtime desc LIMIT 1
    """

    cursor.execute(sql_noise_now)
    noise_now = cursor.fetchall()

    dict = {
        "noise_now": noise_now[0][0],
        "noise_total": noise_now[0][1],
        "data": (float(noise_now[0][0]) / float(noise_now[0][1])) * 100
    }
    conn.close()
    return json.dumps(dict)


# 数字翻牌(今日最高)
@jiangjin.route("/environment/noise_high")
def noise_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_noise_high = """
            SELECT MAX(noise) as max_noise FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_noise_high)
    noise_high = cursor.fetchall()

    dict = {
        "data": noise_high[0][0]
    }
    conn.close()
    return json.dumps(dict)


# echart(全天)
@jiangjin.route("/environment/noise_echart")
def noise_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_noise_echart = """
            SELECT noise as y,DATE_FORMAT(recordtime,'%H:%i') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE order by x
    """

    cursor.execute(sql_noise_echart)
    noise_echart = cursor.fetchall()

    list_x = []
    list_data = []

    for i in noise_echart:
        list_x.append(i[1])
        list_data.append(i[0])

    dict = {
        "x": list_x,
        "y": {"data": list_data}
    }
    conn.close()
    return json.dumps(dict)


# PM2.5
# 平均值
@jiangjin.route("/environment/pm2p5_average")
def pm2p5_average():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_average = """
            SELECT avg(pm2p5) as value FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 

    """

    cursor.execute(sql_average)
    pm2p5_average = cursor.fetchall()

    dict = {
        "data": pm2p5_average[0][0]
    }
    conn.close()
    return json.dumps(dict)


# echart(全天)
@jiangjin.route("/environment/pm2p5_echart")
def pm2p5_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_pm2p5_echart = """
            SELECT pm2p5 as y,DATE_FORMAT(recordtime,'%H:%i') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE order by x
    """

    cursor.execute(sql_pm2p5_echart)
    pm2p5_echart = cursor.fetchall()

    list_x = []
    list_data = []

    for i in pm2p5_echart:
        list_x.append(i[1])
        list_data.append(i[0])

    dict = {
        "x": list_x,
        "y": {"data": list_data}
    }
    conn.close()
    return json.dumps(dict)


# 今日最高
@jiangjin.route("/environment/pm2p5_high")
def pm2p5_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_noise_high = """
            SELECT MAX(pm2p5) as max_pm2p5 FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_noise_high)
    noise_high = cursor.fetchall()

    dict = {
        "data": noise_high[0][0]
    }
    conn.close()
    return json.dumps(dict)


# PM10
# 平均值
@jiangjin.route("/environment/pm10_average")
def pm10_average():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_average = """
            SELECT avg(pm10) as value FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 

    """

    cursor.execute(sql_average)
    pm10_average = cursor.fetchall()

    dict = {
        "data": pm10_average[0][0]
    }
    conn.close()
    return json.dumps(dict)


# echart(全天)
@jiangjin.route("/environment/pm10_echart")
def pm10_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_pm10_echart = """
            SELECT pm10 as y,DATE_FORMAT(recordtime,'%H:%i') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE order by x
    """

    cursor.execute(sql_pm10_echart)
    pm10_echart = cursor.fetchall()

    list_x = []
    list_data = []

    for i in pm10_echart:
        list_x.append(i[1])
        list_data.append(i[0])

    dict = {
        "x": list_x,
        "y": {"data": list_data}
    }
    conn.close()
    return json.dumps(dict)


# 今日最高
@jiangjin.route("/environment/pm10_high")
def pm10_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='openplatform', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_noise_high = """
            SELECT MAX(pm10) as max_pm10 FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_noise_high)
    noise_high = cursor.fetchall()

    dict = {
        "data": noise_high[0][0]
    }
    conn.close()
    return json.dumps(dict)


# 质量安全接口
# 质量管理
# 饼状图
@jiangjin.route("/quality/circle")
def quality_circle():
    url_1 = "http://www.tylinbim.com/wui/qualityProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    solved = []
    unsolved = []
    for i in dataList_1:
        if i["rectificate"] == "是":
            solved.append(i)
        else:
            unsolved.append(i)
    solved_bad = []
    solved_normal = []
    for j in solved:
        if j["serverity"] == "严重":
            solved_bad.append(j)
        else:
            solved_normal.append(j)
    unsolved_bad = []
    unsolved_normal = []
    for k in unsolved:
        if k["serverity"] == "严重":
            unsolved_bad.append(k)
        else:
            unsolved_normal.append(k)

    dict = {"data": {"total": len(dataList_1), "solved": len(solved), "unsolved": len(unsolved),
                     "solved_normal": len(solved_normal), "solved_bad": len(solved_bad),
                     "unsolved_normal": len(unsolved_normal), "unsolved_bad": len(unsolved_bad)}}

    return json.dumps(dict)


# 施工班组质量问题
@jiangjin.route("/quality/team")
def quality_team():
    url_1 = "http://www.tylinbim.com/wui/qualityProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]
    gangjin = []
    muban = []
    qizhuan = []
    fangshui = []
    jiaoshoujia = []
    nuantong = []
    xiaofang = []
    jipaishui = []
    qiangruodian = []
    tadiao = []
    hunningtu = []
    dianhan = []
    unknow = []

    for i in dataList_1:
        if i["team"] == "钢筋班组":
            gangjin.append(i)
        elif i["team"] == "模板班组":
            muban.append(i)
        elif i["team"] == "砌砖班组":
            qizhuan.append(i)
        elif i["team"] == "防水班组":
            fangshui.append(i)
        elif i["team"] == "脚手架班组":
            jiaoshoujia.append(i)
        elif i["team"] == "暖通班组":
            nuantong.append(i)
        elif i["team"] == "消防班组":
            xiaofang.append(i)
        elif i["team"] == "给排水班组":
            jipaishui.append(i)
        elif i["team"] == "强弱电班组":
            qiangruodian.append(i)
        elif i["team"] == "塔吊班组":
            tadiao.append(i)
        elif i["team"] == "混凝土班组":
            hunningtu.append(i)
        elif i["team"] == "电焊班组":
            dianhan.append(i)
        else:
            unknow.append(i)

    dict = {"data": {
        "x": ["钢筋", "模板", "砌砖", "防水", "脚手架", "暖通", "消防", "给排水", "强弱电", "塔吊", "混凝土", "电焊", "未划分"],
        "y": [len(gangjin), len(muban), len(qizhuan), len(fangshui), len(jiaoshoujia), len(nuantong), len(xiaofang),
              len(jipaishui), len(qiangruodian), len(tadiao), len(hunningtu), len(dianhan), len(unknow)]
    }}

    return json.dumps(dict)


# 本周质量问题数量
@jiangjin.route("/quality/week_question")
def quality_week_question():
    url_1 = "http://www.tylinbim.com/wui/qualityProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    datetime_now = datetime.datetime.now()
    today = datetime_now.strftime("%Y-%m-%d")
    last_1_day = (datetime_now - relativedelta(days=1)).strftime("%Y-%m-%d")
    last_2_day = (datetime_now - relativedelta(days=2)).strftime("%Y-%m-%d")
    last_3_day = (datetime_now - relativedelta(days=3)).strftime("%Y-%m-%d")
    last_4_day = (datetime_now - relativedelta(days=4)).strftime("%Y-%m-%d")
    last_5_day = (datetime_now - relativedelta(days=5)).strftime("%Y-%m-%d")
    last_6_day = (datetime_now - relativedelta(days=6)).strftime("%Y-%m-%d")

    today_list = []
    last_1_day_list = []
    last_2_day_list = []
    last_3_day_list = []
    last_4_day_list = []
    last_5_day_list = []
    last_6_day_list = []

    for i in dataList_1:
        if i["checkTime"] == today:
            today_list.append(i)
        elif i["checkTime"] == last_1_day:
            last_1_day_list.append(i)
        elif i["checkTime"] == last_2_day:
            last_2_day_list.append(i)
        elif i["checkTime"] == last_3_day:
            last_3_day_list.append(i)
        elif i["checkTime"] == last_4_day:
            last_4_day_list.append(i)
        elif i["checkTime"] == last_5_day:
            last_5_day_list.append(i)
        elif i["checkTime"] == last_6_day:
            last_6_day_list.append(i)
        else:
            pass

    d1 = (datetime_now - relativedelta(days=6)).strftime("%m/%d")
    d2 = (datetime_now - relativedelta(days=5)).strftime("%m/%d")
    d3 = (datetime_now - relativedelta(days=4)).strftime("%m/%d")
    d4 = (datetime_now - relativedelta(days=3)).strftime("%m/%d")
    d5 = (datetime_now - relativedelta(days=2)).strftime("%m/%d")
    d6 = (datetime_now - relativedelta(days=1)).strftime("%m/%d")
    d7 = last_6_day = datetime_now.strftime("%m/%d")

    dict = {
        "data": {
            "x": [d1, d2, d3, d4, d5, d6, d7],
            "y": [len(last_6_day_list), len(last_5_day_list), len(last_4_day_list), len(last_3_day_list),
                  len(last_2_day_list), len(last_1_day_list), len(today_list)]}
    }

    return json.dumps(dict)


# 本周质量问题统计
@jiangjin.route("/quality/week_question_state")
def quality_week_question_state():
    url_1 = "http://www.tylinbim.com/wui/qualityProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    datetime_now = datetime.datetime.now()
    today = datetime_now.strftime("%Y-%m-%d")
    last_1_day = (datetime_now - relativedelta(days=1)).strftime("%Y-%m-%d")
    last_2_day = (datetime_now - relativedelta(days=2)).strftime("%Y-%m-%d")
    last_3_day = (datetime_now - relativedelta(days=3)).strftime("%Y-%m-%d")
    last_4_day = (datetime_now - relativedelta(days=4)).strftime("%Y-%m-%d")
    last_5_day = (datetime_now - relativedelta(days=5)).strftime("%Y-%m-%d")
    last_6_day = (datetime_now - relativedelta(days=6)).strftime("%Y-%m-%d")

    today_list = []
    last_1_day_list = []
    last_2_day_list = []
    last_3_day_list = []
    last_4_day_list = []
    last_5_day_list = []
    last_6_day_list = []

    today_solved_list = []
    last_1_day_solved_list = []
    last_2_day_solved_list = []
    last_3_day_solved_list = []
    last_4_day_solved_list = []
    last_5_day_solved_list = []
    last_6_day_solved_list = []

    for i in dataList_1:
        if i["checkTime"] == today:
            today_list.append(i)
            if i["rectificate"] == "是":
                today_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_1_day:
            last_1_day_list.append(i)
            if i["rectificate"] == "是":
                last_1_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_2_day:
            last_2_day_list.append(i)
            if i["rectificate"] == "是":
                last_2_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_3_day:
            last_3_day_list.append(i)
            if i["rectificate"] == "是":
                last_3_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_4_day:
            last_4_day_list.append(i)
            if i["rectificate"] == "是":
                last_4_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_5_day:
            last_5_day_list.append(i)
            if i["rectificate"] == "是":
                last_5_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_6_day:
            last_6_day_list.append(i)
            if i["rectificate"] == "是":
                last_6_day_solved_list.append(i)
            else:
                pass
        else:
            pass

    d1 = (datetime_now - relativedelta(days=6)).strftime("%m/%d")
    d2 = (datetime_now - relativedelta(days=5)).strftime("%m/%d")
    d3 = (datetime_now - relativedelta(days=4)).strftime("%m/%d")
    d4 = (datetime_now - relativedelta(days=3)).strftime("%m/%d")
    d5 = (datetime_now - relativedelta(days=2)).strftime("%m/%d")
    d6 = (datetime_now - relativedelta(days=1)).strftime("%m/%d")
    d7 = datetime_now.strftime("%m/%d")

    dict = {
        "data": {
            "x": [d1, d2, d3, d4, d5, d6, d7],
            "total": [len(last_6_day_list), len(last_5_day_list), len(last_4_day_list), len(last_3_day_list),
                      len(last_2_day_list), len(last_1_day_list), len(today_list)],
            "solved": [len(last_6_day_solved_list), len(last_5_day_solved_list), len(last_4_day_solved_list),
                       len(last_3_day_solved_list), len(last_2_day_solved_list), len(last_1_day_solved_list),
                       len(today_solved_list)]}
    }

    return json.dumps(dict)


# 未解决质量问题统计
@jiangjin.route("/quality/unsolved_state")
def quality_unsolved_state():
    url_1 = "http://www.tylinbim.com/wui/qualityProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d")
    today = datetime.datetime.strptime(datetime_now, '%Y-%m-%d')

    d30 = []
    d30_60 = []
    d60_90 = []
    d90_120 = []
    d120 = []
    unsolved = []

    for i in dataList_1:
        if i["rectificate"] == "是":
            pass
        else:
            unsolved.append(i)
            day = str(today - datetime.datetime.strptime(i["checkTime"], '%Y-%m-%d'))
            if day == "0:00:00":
                day = 0
            elif day == "1 day, 0:00:00":
                day = 1
            else:
                day = int(day.replace(" days, 0:00:00", ""))
            if day <= 30:
                d30.append(i)
            elif 30 < day <= 60:
                d30_60.append(i)
            elif 60 < day <= 90:
                d60_90.append(i)
            elif 90 < day <= 120:
                d90_120.append(i)
            elif 120 < day:
                d120.append(i)

    dict = {
        "data": {
            "x": ["<30", "30~60", "60~90", "90~120", ">120"],
            "unsolved": [len(d30), len(d30_60), len(d60_90), len(d90_120), len(d120)],
            "total": [len(d30), len(d30) + len(d30_60), len(d30) + len(d30_60) + len(d60_90),
                      len(d30) + len(d30_60) + len(d60_90) + len(d90_120),
                      len(d30) + len(d30_60) + len(d60_90) + len(d90_120) + len(d120)]
        }
    }

    return json.dumps(dict)


# 安全管理
# 饼状图
@jiangjin.route("/safe/circle")
def safe_circle():
    url_1 = "http://www.tylinbim.com/wui/safeProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    solved = []
    unsolved = []
    for i in dataList_1:
        if i["rectificate"] == "是":
            solved.append(i)
        else:
            unsolved.append(i)
    solved_bad = []
    solved_normal = []
    for j in solved:
        if j["serverity"] == "严重":
            solved_bad.append(j)
        else:
            solved_normal.append(j)
    unsolved_bad = []
    unsolved_normal = []
    for k in unsolved:
        if k["serverity"] == "严重":
            unsolved_bad.append(k)
        else:
            unsolved_normal.append(k)

    dict = {"data": {"total": len(dataList_1), "solved": len(solved), "unsolved": len(unsolved),
                     "solved_normal": len(solved_normal), "solved_bad": len(solved_bad),
                     "unsolved_normal": len(unsolved_normal), "unsolved_bad": len(unsolved_bad)}}

    return json.dumps(dict)


# 施工班组安全问题
@jiangjin.route("/safe/team")
def safe_team():
    url_1 = "http://www.tylinbim.com/wui/safeProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]
    gangjin = []
    muban = []
    qizhuan = []
    fangshui = []
    jiaoshoujia = []
    nuantong = []
    xiaofang = []
    jipaishui = []
    qiangruodian = []
    tadiao = []
    hunningtu = []
    dianhan = []
    unknow = []

    for i in dataList_1:
        if i["team"] == "钢筋班组":
            gangjin.append(i)
        elif i["team"] == "模板班组":
            muban.append(i)
        elif i["team"] == "砌砖班组":
            qizhuan.append(i)
        elif i["team"] == "防水班组":
            fangshui.append(i)
        elif i["team"] == "脚手架班组":
            jiaoshoujia.append(i)
        elif i["team"] == "暖通班组":
            nuantong.append(i)
        elif i["team"] == "消防班组":
            xiaofang.append(i)
        elif i["team"] == "给排水班组":
            jipaishui.append(i)
        elif i["team"] == "强弱电班组":
            qiangruodian.append(i)
        elif i["team"] == "塔吊班组":
            tadiao.append(i)
        elif i["team"] == "混凝土班组":
            hunningtu.append(i)
        elif i["team"] == "电焊班组":
            dianhan.append(i)
        else:
            unknow.append(i)

    dict = {"data": {
        "x": ["钢筋", "模板", "砌砖", "防水", "脚手架", "暖通", "消防", "给排水", "强弱电", "塔吊", "混凝土", "电焊", "未划分"],
        "y": [len(gangjin), len(muban), len(qizhuan), len(fangshui), len(jiaoshoujia), len(nuantong), len(xiaofang),
              len(jipaishui), len(qiangruodian), len(tadiao), len(hunningtu), len(dianhan), len(unknow)]
    }}

    return json.dumps(dict)


# 本周质量问题数量
@jiangjin.route("/safe/week_question")
def safe_week_question():
    url_1 = "http://www.tylinbim.com/wui/safeProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    datetime_now = datetime.datetime.now()
    today = datetime_now.strftime("%Y-%m-%d")
    last_1_day = (datetime_now - relativedelta(days=1)).strftime("%Y-%m-%d")
    last_2_day = (datetime_now - relativedelta(days=2)).strftime("%Y-%m-%d")
    last_3_day = (datetime_now - relativedelta(days=3)).strftime("%Y-%m-%d")
    last_4_day = (datetime_now - relativedelta(days=4)).strftime("%Y-%m-%d")
    last_5_day = (datetime_now - relativedelta(days=5)).strftime("%Y-%m-%d")
    last_6_day = (datetime_now - relativedelta(days=6)).strftime("%Y-%m-%d")

    today_list = []
    last_1_day_list = []
    last_2_day_list = []
    last_3_day_list = []
    last_4_day_list = []
    last_5_day_list = []
    last_6_day_list = []

    for i in dataList_1:
        if i["checkTime"] == today:
            today_list.append(i)
        elif i["checkTime"] == last_1_day:
            last_1_day_list.append(i)
        elif i["checkTime"] == last_2_day:
            last_2_day_list.append(i)
        elif i["checkTime"] == last_3_day:
            last_3_day_list.append(i)
        elif i["checkTime"] == last_4_day:
            last_4_day_list.append(i)
        elif i["checkTime"] == last_5_day:
            last_5_day_list.append(i)
        elif i["checkTime"] == last_6_day:
            last_6_day_list.append(i)
        else:
            pass

    d1 = (datetime_now - relativedelta(days=6)).strftime("%m/%d")
    d2 = (datetime_now - relativedelta(days=5)).strftime("%m/%d")
    d3 = (datetime_now - relativedelta(days=4)).strftime("%m/%d")
    d4 = (datetime_now - relativedelta(days=3)).strftime("%m/%d")
    d5 = (datetime_now - relativedelta(days=2)).strftime("%m/%d")
    d6 = (datetime_now - relativedelta(days=1)).strftime("%m/%d")
    d7 = last_6_day = datetime_now.strftime("%m/%d")

    dict = {
        "data": {
            "x": [d1, d2, d3, d4, d5, d6, d7],
            "y": [len(last_6_day_list), len(last_5_day_list), len(last_4_day_list), len(last_3_day_list),
                  len(last_2_day_list), len(last_1_day_list), len(today_list)]}
    }

    return json.dumps(dict)


# 本周质量问题统计
@jiangjin.route("/safe/week_question_state")
def safe_week_question_state():
    url_1 = "http://www.tylinbim.com/wui/safeProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    datetime_now = datetime.datetime.now()
    today = datetime_now.strftime("%Y-%m-%d")
    last_1_day = (datetime_now - relativedelta(days=1)).strftime("%Y-%m-%d")
    last_2_day = (datetime_now - relativedelta(days=2)).strftime("%Y-%m-%d")
    last_3_day = (datetime_now - relativedelta(days=3)).strftime("%Y-%m-%d")
    last_4_day = (datetime_now - relativedelta(days=4)).strftime("%Y-%m-%d")
    last_5_day = (datetime_now - relativedelta(days=5)).strftime("%Y-%m-%d")
    last_6_day = (datetime_now - relativedelta(days=6)).strftime("%Y-%m-%d")

    today_list = []
    last_1_day_list = []
    last_2_day_list = []
    last_3_day_list = []
    last_4_day_list = []
    last_5_day_list = []
    last_6_day_list = []

    today_solved_list = []
    last_1_day_solved_list = []
    last_2_day_solved_list = []
    last_3_day_solved_list = []
    last_4_day_solved_list = []
    last_5_day_solved_list = []
    last_6_day_solved_list = []

    for i in dataList_1:
        if i["checkTime"] == today:
            today_list.append(i)
            if i["rectificate"] == "是":
                today_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_1_day:
            last_1_day_list.append(i)
            if i["rectificate"] == "是":
                last_1_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_2_day:
            last_2_day_list.append(i)
            if i["rectificate"] == "是":
                last_2_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_3_day:
            last_3_day_list.append(i)
            if i["rectificate"] == "是":
                last_3_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_4_day:
            last_4_day_list.append(i)
            if i["rectificate"] == "是":
                last_4_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_5_day:
            last_5_day_list.append(i)
            if i["rectificate"] == "是":
                last_5_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"] == last_6_day:
            last_6_day_list.append(i)
            if i["rectificate"] == "是":
                last_6_day_solved_list.append(i)
            else:
                pass
        else:
            pass

    d1 = (datetime_now - relativedelta(days=6)).strftime("%m/%d")
    d2 = (datetime_now - relativedelta(days=5)).strftime("%m/%d")
    d3 = (datetime_now - relativedelta(days=4)).strftime("%m/%d")
    d4 = (datetime_now - relativedelta(days=3)).strftime("%m/%d")
    d5 = (datetime_now - relativedelta(days=2)).strftime("%m/%d")
    d6 = (datetime_now - relativedelta(days=1)).strftime("%m/%d")
    d7 = datetime_now.strftime("%m/%d")

    dict = {
        "data": {
            "x": [d1, d2, d3, d4, d5, d6, d7],
            "total": [len(last_6_day_list), len(last_5_day_list), len(last_4_day_list), len(last_3_day_list),
                      len(last_2_day_list), len(last_1_day_list), len(today_list)],
            "solved": [len(last_6_day_solved_list), len(last_5_day_solved_list), len(last_4_day_solved_list),
                       len(last_3_day_solved_list), len(last_2_day_solved_list), len(last_1_day_solved_list),
                       len(today_solved_list)]}
    }

    return json.dumps(dict)


# 未解决质量问题统计
@jiangjin.route("/safe/unsolved_state")
def safe_unsolved_state():
    url_1 = "http://www.tylinbim.com/wui/safeProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d")
    today = datetime.datetime.strptime(datetime_now, '%Y-%m-%d')

    d30 = []
    d30_60 = []
    d60_90 = []
    d90_120 = []
    d120 = []
    unsolved = []

    for i in dataList_1:
        if i["rectificate"] == "是":
            pass
        else:
            unsolved.append(i)
            day = str(today - datetime.datetime.strptime(i["checkTime"], '%Y-%m-%d'))
            if day == "0:00:00":
                day = 0
            elif day == "1 day, 0:00:00":
                day = 1
            else:
                day = int(day.replace(" days, 0:00:00", ""))
            if day <= 30:
                d30.append(i)
            elif 30 < day <= 60:
                d30_60.append(i)
            elif 60 < day <= 90:
                d60_90.append(i)
            elif 90 < day <= 120:
                d90_120.append(i)
            elif 120 < day:
                d120.append(i)

    dict = {
        "data": {
            "x": ["<30", "30~60", "60~90", "90~120", ">120"],
            "unsolved": [len(d30), len(d30_60), len(d60_90), len(d90_120), len(d120)],
            "total": [len(d30), len(d30) + len(d30_60), len(d30) + len(d30_60) + len(d60_90),
                      len(d30) + len(d30_60) + len(d60_90) + len(d90_120),
                      len(d30) + len(d30_60) + len(d60_90) + len(d90_120) + len(d120)]
        }
    }

    return json.dumps(dict)


# 晴雨表
@jiangjin.route("/weather_list")
def jiangjin_weather_data():
    dict = {"data": {"url": "http://183.66.213.82:8888/weatherlist/jiangjin"}}
    return json.dumps(dict)