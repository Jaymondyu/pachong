#coding:utf-8
from flask import Flask,request,render_template
import mysql.connector
import json
import time
import datetime
import requests
from dateutil.relativedelta import relativedelta
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# 江津数据库
conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='openplatform',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()
# shenzhen_event 数据库
conn_yuelai_event = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='shenzhen_event',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor_yuelai_event = conn_yuelai_event.cursor()

app = Flask(__name__)

# 江津滨江新城大屏
@app.route("/jiangjin")
def jiangjin():
    return render_template("jiangjin_index.html")
@app.route("/jiangjin/insert")
def jiangjin_insert():
    return render_template("jiangjin_insert.html")

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
        "pm2p5":enviroment[0][0],
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
                        DATE_FORMAT(attendancetime, '%m-%d') AS x,
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

    return json.dumps(dict)


# 安全问题
@app.route("/jiangjin/index/anquan")
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
            month_now_solved.append(k)
    for l in month_2_before:
        if l["rectificate"] == "是":
            month_now_solved.append(l)
    for m in month_3_before:
        if m["rectificate"] == "是":
            month_now_solved.append(m)
    for n in month_4_before:
        if n["rectificate"] == "是":
            month_now_solved.append(n)

    y = {
        "total": [len(month_4_before), len(month_3_before), len(month_2_before), len(month_1_before), len(month_now)],
        "solved": [len(month_4_before_solved), len(month_3_before_solved), len(month_2_before_solved),
                   len(month_1_before_solved), len(month_now_solved)]
    }
    x = [last_4_month, last_3_month, last_2_month, last_1_month, this_month]

    dict = {"y": y, "x": x}

    return json.dumps(dict)

# 质量问题
@app.route("/jiangjin/index/zhiliang")
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
            month_now_solved.append(k)
    for l in month_2_before:
        if l["rectificate"] == "是":
            month_now_solved.append(l)
    for m in month_3_before:
        if m["rectificate"] == "是":
            month_now_solved.append(m)
    for n in month_4_before:
        if n["rectificate"] == "是":
            month_now_solved.append(n)

    y = {
        "total": [len(month_4_before), len(month_3_before), len(month_2_before), len(month_1_before), len(month_now)],
        "solved": [len(month_4_before_solved), len(month_3_before_solved), len(month_2_before_solved),
                   len(month_1_before_solved), len(month_now_solved)]
    }
    x = [last_4_month, last_3_month, last_2_month, last_1_month, this_month]

    dict = {"y": y, "x": x}

    return json.dumps(dict)
# 进度
@app.route("/jiangjin/index/jindu")
def jindu():
    sql_jindu = "select tujian,xuanwazhuang,wakongzhuang,jidian,muqiang,jingzhuang,shiwaigongcheng from jiangjin_screen where tujian is not NULL order by id desc LIMIT 1"
    cursor.execute(sql_jindu)
    jindu = cursor.fetchall()


    list = [
        {"data": jindu[0][0],
         "name":"土建工程"},
        {"comp": jindu[0][1],
         "total":227,
         "data":float(jindu[0][1])/227*100,
         "name":"旋挖桩"},
        {"comp": jindu[0][2],
         "total": 190,
         "data":float(jindu[0][2])/190*100,
         "name":"挖孔桩"},
        {"data": jindu[0][3],
         "name":"机电工程"},
        {"data": jindu[0][4],
         "name":"幕墙工程"},
        {"data": jindu[0][5],
         "name":"精装工程"},
        {"data": jindu[0][6],
         "name":"室外工程"}
    ]
    return json.dumps(list)
# 进度上传
@app.route("/jiangjin/index/jindu_insert",methods=["POST"])
def jindu_insert():
    data = request.get_json()
    tujian = data["tujian"]
    xuanwazhuang = data["xuanwazhuang"]
    wakongzhuang = data["wakongzhuang"]
    jidian = data["jidian"]
    muqiang = data["muqiang"]
    jingzhuang = data["jingzhuang"]
    shiwaigongcheng = data["shiwaigongcheng"]

    insert = """
        insert into jiangjin_screen (tujian,xuanwazhuang,wakongzhuang,jidian,muqiang,jingzhuang,shiwaigongcheng)
        values (%d,%d,%d,%d,%d,%d,%d)
    """%(tujian,xuanwazhuang,wakongzhuang,jidian,muqiang,jingzhuang,shiwaigongcheng)

    cursor.execute(insert)
    conn.commit()


    return "data inserted"

# 项目概况
@app.route("/jiangjin/index/intro")
def intro():
    dict={ "data" :"本项目位于重庆市江津区滨江新城核心区A7-07-2/01地块，新建项目用地北侧及西侧紧邻城市道路，交通便捷，东侧与未建居住用地相临，南侧与公园绿地相临并有城市高压线。本项目总建筑面积91342.37m2，其中地上面积67040.15m2，地下面积24302.22 m2。地上建筑主要由行政办公、商务办公A栋及其裙房行政服务中心、商务办公B栋组成，地下部分主要为地下车库及设备用房。行政办公、商务办公均为二类高层公共建筑，属二类办公建筑，行政服务中心为高层建筑裙房，耐火等级均为一级，地下车库为I类停车库，耐火等级为一级,本工程地势为南高北低，标高在256.7~269.0米之间；高差约13米，结构主体采用框架结构体系。"}
    return json.dumps(dict)
# 参建单位
@app.route("/jiangjin/index/company")
def company():
    list=[
        {
            "unit": "建设单位",
            "company": "重庆市江津区滨江新城开发建设集团有限公司"
        },
        {
            "unit":"勘察单位",
            "company":"重庆市设计院"
        },{
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
# 专业分包
@app.route("/jiangjin/renyuan/zhuanyefenbao")
def zhuanyefenbao():
    sql_zhuanyefenbao = """
            SELECT name, department,if(entry=1,'进场','出场') as entry, DATE_FORMAT(attendancetime,'%Y-%m-%d %H:%i:%s') as attendancetime 
            from access 
            where DATE_FORMAT(attendancetime,'%Y-%m-%d') = date_format(CURRENT_DATE,'%Y-%m-%d') 
            AND department in ('重庆正旋基础有限公司','重庆名庆防水工程有限公司','重庆力杰消防工程有限公司')

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

    return json.dumps(list)
#人员统计
@app.route("/jiangjin/renyuan/renyuantongji")
def renyuantongji():
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
	(select name,department, DATE_FORMAT(attendancetime, '%Y-%m-%d') as attendancetime from access
WHERE
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
        "x":list_x,
        "y":[{"name":"重庆建工住宅建设有限公司","data":list_3},{"name":"重庆正旋基础有限公司","data":list_2},{"name":"重庆联文建筑劳务有限公司","data":list_1},{"name":"林同棪【重庆】国际工程技术有限公司","data":list_4},{"name":"重庆名庆防水工程有限公司","data":list_5},{"name":"重庆力杰消防工程有限公司","data":list_6}]

    }


    return json.dumps(dict)


# 环境监测接口
# 风速
# 圆环(当前)
@app.route("/jiangjin/environment/wind_now")
def wind_now():
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
        "wind_now":wind_now_1,
        "wind_total": wind_now[0][1],
        "data":(float(wind_now_1)/float(wind_now[0][1]))*100
    }
    return json.dumps(dict)
# 数字翻牌(今日最高)
@app.route("/jiangjin/environment/wind_high")
def wind_high():
    sql_wind_high = """
            SELECT MAX(windspeed) as max_windspeed FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_wind_high)
    wind_high = cursor.fetchall()

    dict ={
        "data":wind_high[0][0]
    }

    return json.dumps(dict)
# echart(全天)
@app.route("/jiangjin/environment/wind_echart")
def wind_echart():
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

    for data in range(0,len(list_data)):
        if str(type(list_data[data])) == "<type 'NoneType'>":
            list_data[data] = 0.0


    dict = {
        "x": list_x,
        "y":{"data":list_data}
    }

    return json.dumps(dict)

# 湿度
# 圆环(当前)
@app.route("/jiangjin/environment/humidity_now")
def humidity_now():
    sql_humidity_now = """
            select humidity as actual,100 as aims from environment order by recordtime desc LIMIT 1
    """

    cursor.execute(sql_humidity_now)
    humidity_now = cursor.fetchall()

    dict = {
        "humidity_now":humidity_now[0][0],
        "humidity_total": humidity_now[0][1],
        "data":(float(humidity_now[0][0])/float(humidity_now[0][1]))*100
    }
    return json.dumps(dict)
# 数字翻牌(今日最高)
@app.route("/jiangjin/environment/humidity_high")
def humidity_high():
    sql_humidity_high = """
            SELECT MAX(humidity) as max_humidity FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_humidity_high)
    humidity_high = cursor.fetchall()

    dict ={
        "data":humidity_high[0][0]
    }

    return json.dumps(dict)
# echart(全天)
@app.route("/jiangjin/environment/humidity_echart")
def humidity_echart():
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
        "y":{"data":list_data}
    }

    return json.dumps(dict)

# 温度
# 圆环(当前)
@app.route("/jiangjin/environment/temperature_now")
def temperature_now():
    sql_temperature_now = """
            select temperature as actual,50 as aims from environment order by recordtime desc LIMIT 1
    """

    cursor.execute(sql_temperature_now)
    temperature_now = cursor.fetchall()

    dict = {
        "temperature_now":temperature_now[0][0],
        "temperature_total": temperature_now[0][1],
        "data":(float(temperature_now[0][0])/float(temperature_now[0][1]))*100
    }
    return json.dumps(dict)
# 数字翻牌(今日最高)
@app.route("/jiangjin/environment/temperature_high")
def temperature_high():
    sql_temperature_high = """
            SELECT MAX(temperature) as max_temperature FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_temperature_high)
    temperature_high = cursor.fetchall()

    dict ={
        "data":temperature_high[0][0]
    }

    return json.dumps(dict)
# echart(全天)
@app.route("/jiangjin/environment/temperature_echart")
def temperature_echart():
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
        "y":{"data":list_data}
    }

    return json.dumps(dict)

# 噪音
# 圆环(当前)
@app.route("/jiangjin/environment/noise_now")
def noise_now():
    sql_noise_now = """
            select noise as actual,140 as aims from environment order by recordtime desc LIMIT 1
    """

    cursor.execute(sql_noise_now)
    noise_now = cursor.fetchall()

    dict = {
        "noise_now":noise_now[0][0],
        "noise_total": noise_now[0][1],
        "data":(float(noise_now[0][0])/float(noise_now[0][1]))*100
    }
    return json.dumps(dict)
# 数字翻牌(今日最高)
@app.route("/jiangjin/environment/noise_high")
def noise_high():
    sql_noise_high = """
            SELECT MAX(noise) as max_noise FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_noise_high)
    noise_high = cursor.fetchall()

    dict ={
        "data":noise_high[0][0]
    }

    return json.dumps(dict)
# echart(全天)
@app.route("/jiangjin/environment/noise_echart")
def noise_echart():
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
        "y":{"data":list_data}
    }

    return json.dumps(dict)

# PM2.5
# 平均值
@app.route("/jiangjin/environment/pm2p5_average")
def pm2p5_average():
    sql_average = """
            SELECT avg(pm2p5) as value FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 

    """


    cursor.execute(sql_average)
    pm2p5_average = cursor.fetchall()

    dict ={
        "data":pm2p5_average[0][0]
    }

    return json.dumps(dict)
# echart(全天)
@app.route("/jiangjin/environment/pm2p5_echart")
def pm2p5_echart():
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
        "y":{"data":list_data}
    }

    return json.dumps(dict)
# 今日最高
@app.route("/jiangjin/environment/pm2p5_high")
def pm2p5_high():
    sql_noise_high = """
            SELECT MAX(pm2p5) as max_pm2p5 FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_noise_high)
    noise_high = cursor.fetchall()

    dict ={
        "data":noise_high[0][0]
    }

    return json.dumps(dict)

# PM10
# 平均值
@app.route("/jiangjin/environment/pm10_average")
def pm10_average():
    sql_average = """
            SELECT avg(pm10) as value FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 

    """


    cursor.execute(sql_average)
    pm10_average = cursor.fetchall()

    dict ={
        "data":pm10_average[0][0]
    }

    return json.dumps(dict)
# echart(全天)
@app.route("/jiangjin/environment/pm10_echart")
def pm10_echart():
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
        "y":{"data":list_data}
    }

    return json.dumps(dict)
# 今日最高
@app.route("/jiangjin/environment/pm10_high")
def pm10_high():
    sql_noise_high = """
            SELECT MAX(pm10) as max_pm10 FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE 
    """

    cursor.execute(sql_noise_high)
    noise_high = cursor.fetchall()

    dict ={
        "data":noise_high[0][0]
    }

    return json.dumps(dict)


# 质量安全接口
# 质量管理
# 饼状图
@app.route("/jiangjin/quality/circle")
def quality_circle():

    url_1 = "http://www.tylinbim.com/wui/qualityProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    solved = []
    unsolved =[]
    for i in dataList_1:
        if i["rectificate"] == "是":
            solved.append(i)
        else:
            unsolved.append(i)
    solved_bad =[]
    solved_normal = []
    for j in solved:
        if j["serverity"] == "严重":
            solved_bad.append(j)
        else:
            solved_normal.append(j)
    unsolved_bad =[]
    unsolved_normal = []
    for k in unsolved:
        if k["serverity"] == "严重":
            unsolved_bad.append(k)
        else:
            unsolved_normal.append(k)

    dict = {"data":{"total":len(dataList_1),"solved":len(solved),"unsolved":len(unsolved),"solved_normal":len(solved_normal),"solved_bad":len(solved_bad),"unsolved_normal":len(unsolved_normal),"unsolved_bad":len(unsolved_bad)}}


    return json.dumps(dict)

# 施工班组质量问题
@app.route("/jiangjin/quality/team")
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

    dict ={"data":{
                   "x":["钢筋","模板","砌砖","防水","脚手架","暖通","消防","给排水","强弱电","塔吊","混凝土","电焊","未划分"],
                   "y":[len(gangjin),len(muban),len(qizhuan),len(fangshui),len(jiaoshoujia),len(nuantong),len(xiaofang),len(jipaishui),len(qiangruodian),len(tadiao),len(hunningtu),len(dianhan),len(unknow)]
          }}

    return json.dumps(dict)

# 安全管理
# 饼状图
@app.route("/jiangjin/safe/circle")
def safe_circle():

    url_1 = "http://www.tylinbim.com/wui/safeProList"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    solved = []
    unsolved =[]
    for i in dataList_1:
        if i["rectificate"] == "是":
            solved.append(i)
        else:
            unsolved.append(i)
    solved_bad =[]
    solved_normal = []
    for j in solved:
        if j["serverity"] == "严重":
            solved_bad.append(j)
        else:
            solved_normal.append(j)
    unsolved_bad =[]
    unsolved_normal = []
    for k in unsolved:
        if k["serverity"] == "严重":
            unsolved_bad.append(k)
        else:
            unsolved_normal.append(k)

    dict = {"data":{"total":len(dataList_1),"solved":len(solved),"unsolved":len(unsolved),"solved_normal":len(solved_normal),"solved_bad":len(solved_bad),"unsolved_normal":len(unsolved_normal),"unsolved_bad":len(unsolved_bad)}}


    return json.dumps(dict)

# 施工班组安全问题
@app.route("/jiangjin/safe/team")
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

    dict ={"data":{
                   "x":["钢筋","模板","砌砖","防水","脚手架","暖通","消防","给排水","强弱电","塔吊","混凝土","电焊","未划分"],
                   "y":[len(gangjin),len(muban),len(qizhuan),len(fangshui),len(jiaoshoujia),len(nuantong),len(xiaofang),len(jipaishui),len(qiangruodian),len(tadiao),len(hunningtu),len(dianhan),len(unknow)]
          }}

    return json.dumps(dict)









# 晴雨表
@app.route("/jiangjin/weather_table/editdata",methods=["POST"])
def jiangjin_EditData():

    data = request.get_json()
    project_name = "江津滨江新城"
    date = data["date"]
    weather = data["weather"]
    warning = data["warning"]

    sql_insert = """
                insert into weather_table (project_name,date,weather,warning) values ("%s","%s",%d,%d)
    """%(project_name,date,weather,warning)


    conn_yuelai_event.cursor(sql_insert)
    conn_yuelai_event.commit()

    return "200"

@app.route("/jiangjin/weather_table/data")
def jiangjin_weather_data():

    sql_table = """
                    SELECT date,weather,warning from weather_table where project_name = '江津滨江新城'
    """

    cursor_yuelai_event.execute(sql_table)
    result = cursor_yuelai_event.fetchall()

    list = []
    for i in result:
        date = i[0].strftime('%Y-%m-%d')
        weather = i[1]
        warning = i[2]
        dict = {"date":date,"weather":weather,"warning":warning}
        list.append(dict)

    final_dict = {"data":list}
    return json.dumps(final_dict)




# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------- 分割线 ------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# 悦来会展总部基地项目大屏





# 驾驶舱
@app.route("/yuelai")
def yuelai():
    return render_template("index_yuelai.html")
# 天气
@app.route("/yuelai/index/weather")
def yuelai_index_weather():
    # 数据库查询
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
    return json.dumps(list)
#资产统计
@app.route("/yuelai/index/zichan")
def yuelai_index_renyuan():
    dict = {
        "x":["8月第1周","8月第2周","8月第3周","8月第4周"],
        "y":[{"name":"计划产值","data":[200,400,450,500]},{"name":"实际产值","data":[150,350,400,450]}]
    }
    return json.dumps(dict)
# 进度
@app.route("/yuelai/index/jindu")
def yuelai_jindu():
    sql_jindu = "select tujian,xuanwazhuang,wakongzhuang,jidian,muqiang,jingzhuang,shiwaigongcheng from jiangjin_screen where tujian is not NULL order by id desc LIMIT 1"
    cursor.execute(sql_jindu)
    jindu = cursor.fetchall()


    list = [
        {"data": jindu[0][0],
         "name":"土建工程"},
        {"comp": jindu[0][1],
         "total":227,
         "data":float(jindu[0][1])/227*100,
         "name":"旋挖桩"},
        {"comp": jindu[0][2],
         "total": 190,
         "data":float(jindu[0][2])/190*100,
         "name":"挖孔桩"},
        {"data": jindu[0][3],
         "name":"机电工程"},
        {"data": jindu[0][4],
         "name":"幕墙工程"},
        {"data": jindu[0][5],
         "name":"精装工程"},
        {"data": jindu[0][6],
         "name":"室外工程"}
    ]
    return json.dumps(list)

# 项目概况
@app.route("/yuelai/index/intro")
def yuelai_intro():
    dict = {"data":{
        "data": """    项目紧邻悦来国博会展中心及会展公园，是国博会展中心重要的配套项目。项目以实现绿色建筑三星、LEED金级标准为设计目标，旨在打造一个集智能、绿色、时尚为一体的具有新区特色和时代风貌的文化艺术城市综合体，成为悦来会展城重要地标性建筑，也将成为绿色建筑、智能建筑的典范工程。
    项目总用地面积20904.00㎡，容积率6.0，建筑密度40%，绿地率30%.总建筑面积204204.60 ㎡，其中计容建筑面积125424.00㎡，地上建筑面积162609.28 ㎡，地下建筑面积41595.32 ㎡。建筑最高195.67m。由一栋23层的高层塔楼、一栋43层的超高层塔楼及裙房组成，地下吊2层，负6层为设备用房及车库。高层塔楼功能为雅辰酒店，约384间客房；超高层部分吊1层至34层功能为办公（其中1层、17层为酒店大堂），35层至43层为洲际集团旗下英迪格酒店，约200间客房，裙房为配套商业。              
    """
    }}
    return json.dumps(dict)
# 参建单位
@app.route("/yuelai/index/company")
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
@app.route("/yuelai/index/pic")
def yuelai_pic():
    list={
       "data":{"data":[{"url":"http://183.66.213.82:8888/screen/static/yuelai_pic/1.png"},{"url":"http://183.66.213.82:8888/screen/static/yuelai_pic/2.png"},{"url":"http://183.66.213.82:8888/screen/static/yuelai_pic/3.png"}]}
    }
    return json.dumps(list)
# 无人机地址
@app.route("/yuelai/index/wurenji")
def yuelai_wurenji():
    dict = {"data":
        {"data":"https://720yun.com/t/e8vknmdlr7l"}
    }
    return json.dumps(dict)
# 模型(左)地址
@app.route("/yuelai/index/iframe_left")
def yuelai_iframe_left():
    dict = {"data":
        {"data":"http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=UnIv6b"}
    }
    return json.dumps(dict)
# 模型(右)地址
@app.route("/yuelai/index/iframe_right")
def yuelai_iframe_right():
    dict = {"data":
        {"data":"http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=mEfui2"}
    }
    return json.dumps(dict)




# 计划追踪
# 全部
@app.route('/yuelai/event/table',methods=["POST"]) #dpi,page
def table():
    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]

    if dpi== "0":


        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id LIMIT "+ str((page-1)*10)+',10'

        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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

        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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
    return json.dumps(final_dict)
# 滞后
@app.route('/yuelai/event/table/late',methods=["POST"]) #dpi,page
def late():
    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]

    if dpi== "0":

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time) >0 and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where event.dpi=" + dpi + " and datediff(CURRENT_DATE , plan_time) >0 and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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
    return json.dumps(final_dict)
# 临近
@app.route('/yuelai/event/table/near',methods=["POST"]) #dpi,page
def near():
    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]

    if dpi== "0":

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time) between -3 and 0  and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where event.dpi=" + dpi + " and datediff(CURRENT_DATE , plan_time) between -3 and 0  and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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
    return json.dumps(final_dict)
# 已完成
@app.route('/yuelai/event/table/complete',methods=["POST"]) #dpi,page
def complete():

    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]



    if dpi=="0":

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where finish_time is not null LIMIT " + str((page-1)*10) + ',10'
        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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
        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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
    return json.dumps(final_dict)
# 计划内
@app.route('/yuelai/event/table/in_plan',methods=["POST"]) #dpi,page
def in_plan():

    data = request.get_json()
    dpi = data["dpi"]
    page = data["page"]

    if dpi=="0":

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where datediff(CURRENT_DATE , plan_time)<-3  and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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
        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where event.dpi=" + dpi + " and datediff(CURRENT_DATE , plan_time)<-3  and finish_time is null LIMIT " + str((page - 1) * 10) + ',10'
        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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
    return json.dumps(final_dict)
# 总数获取
@app.route('/yuelai/event/table/count')
def count():
    #数据库查询语句(通用)

    complete_data = 'SELECT event.id from event where finish_time is not null '
    in_plan_data = "SELECT event.id from event where datediff(CURRENT_DATE , plan_time)<-3 and finish_time is null"
    near_data = "SELECT event.id from event where datediff(CURRENT_DATE , plan_time) between -3 and 0 and finish_time is null"
    late_data = "SELECT event.id from event where datediff(CURRENT_DATE , plan_time)>0 and finish_time is null"

    #查找已完成:
    cursor_yuelai_event.execute(complete_data)
    complete = cursor_yuelai_event.fetchall()
    #查找计划中:
    cursor_yuelai_event.execute(in_plan_data)
    in_plan = cursor_yuelai_event.fetchall()
    # 查找临近:
    cursor_yuelai_event.execute(near_data)
    near = cursor_yuelai_event.fetchall()
    # 查找滞后:
    cursor_yuelai_event.execute(late_data)
    late = cursor_yuelai_event.fetchall()
    #统一封装:
    count_dict = {"late":len(late),"near":len(near),"in_plan":len(in_plan),"complete":len(complete)}
    count_list =[]
    count_list.append(count_dict)
    final_dict = {"data":count_dict}
    return json.dumps(final_dict)
# 页数
@app.route('/yuelai/event/table/page',methods=['POST']) #dpi
def page():
    data = request.get_json()
    dpi = data["dpi"]

    if dpi == "0":

        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id"

        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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
        table = "SELECT event.id,event_name, start_plan ,plan_time, finish_time, department,name from event JOIN person ON event.dpi=person.id where event.dpi=" + dpi

        cursor_yuelai_event.execute(table)

        result = cursor_yuelai_event.fetchall()

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
    return json.dumps(dict)





#---------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------

# 江苏园博园大屏

@app.route("/jiangsu/pic")
def jiangsu_pic():
    return render_template("jiangsu_pic.html")













application = app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888, debug=True)