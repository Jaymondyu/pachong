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
@app.route("/jiangjin")
def jiangjin():
    return render_template("index.html")

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
        }, {
            "unit": "设计单位",
            "company": "重庆市设计院"
        }, {
            "unit": "施工总包单位",
            "company": "重庆建工住宅建设有限公司"
        }, {
            "unit": "监理单位",
            "company": "林同棪（重庆）国际工程技术有限公司"
        }, {
            "unit": "BIM咨询单位",
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
            AND department in ('重庆正旋基础有限公司','重庆名庆防水工程有限公司')

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
	DATE_FORMAT(attendancetime, '%Y-%m-%d') AS x,
	CASE
WHEN department = "重庆建工住宅建设有限公司" THEN
	1
WHEN department = "重庆正旋基础有限公司" THEN
	2
WHEN department = "重庆联文建筑劳务有限公司" THEN
	3
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

    list_x = []
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
    for i in renyuantongji:
        list_x.append(i[1])
        if i[2] == 1:
            list_1.append(i[0])
        elif i[2] == 2:
            list_2.append(i[0])
        elif i[2] == 3:
            list_3.append(i[0])
        elif i[2] == 4:
            list_4.append(i[0])
        elif i[2] == 5:
            list_5.append(i[0])
        elif i[2] == 6:
            list_6.append(i[0])

    dict = {
        "x":list_x[0:7],
        "y":[{"name":"重庆建工住宅建设有限公司","data":list_1},{"name":"重庆正旋基础有限公司","data":list_2},{"name":"重庆联文建筑劳务有限公司","data":list_3},{"name":"林同棪【重庆】国际工程技术有限公司","data":list_4},{"name":"重庆名庆防水工程有限公司","data":list_5},{"name":"重庆力杰消防工程有限公司","data":list_6}]

    }

    return json.dumps(dict)


# 环境监测接口
# 风速
# 圆环(当前)
@app.route("/jiangjin/environment/wind_now")
def wind_now():
    sql_wind_now = """
            select windspeed as actual,10 as aims from environment order by id desc LIMIT 1
    """

    cursor.execute(sql_wind_now)
    wind_now = cursor.fetchall()

    dict = {
        "wind_now":wind_now[0][0],
        "wind_total": wind_now[0][1],
        "data":(float(wind_now[0][0])/float(wind_now[0][1]))*100
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
            SELECT windspeed as y,DATE_FORMAT(recordtime,'%T') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE
    """

    cursor.execute(sql_wind_echart)
    wind_echart = cursor.fetchall()

    list_x = []
    list_data = []

    for i in wind_echart:
        list_x.append(i[1])
        list_data.append(i[0])

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
            select humidity as actual,100 as aims from environment order by id desc LIMIT 1
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
            SELECT humidity as y,DATE_FORMAT(recordtime,'%T') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE
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
            select temperature as actual,50 as aims from environment order by id desc LIMIT 1
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
            SELECT temperature as y,DATE_FORMAT(recordtime,'%T') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE
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
            select noise as actual,140 as aims from environment order by id desc LIMIT 1
    """

    cursor.execute(sql_noise_now)
    noise_now = cursor.fetchall()

    dict = {
        "temperature_now":noise_now[0][0],
        "temperature_total": noise_now[0][1],
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
            SELECT noise as y,DATE_FORMAT(recordtime,'%T') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE
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
            SELECT pm2p5 as y,DATE_FORMAT(recordtime,'%T') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE
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
            SELECT pm10 as y,DATE_FORMAT(recordtime,'%T') as x FROM environment where DATE_FORMAT(recordtime,'%Y-%m-%d')= CURRENT_DATE
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


# 安全管理接口
@app.route("/jiangjin/safe/list")
def list():
    list = [
        {
            "q": "施工许可证"
        },
        {
            "q": "危大工程管理及安全技术交底"
        },
        {
            "q": "安全专项施工方案及专家论证"
        },
        {
            "q": "人员履职及人员变更"
        },
        {
            "q": "无证上岗"
        },
        {
            "q": "机械违规使用"
        },
        {
            "q": "安全检查"
        },
        {
            "q": "安全资料"
        },
        {
            "q": "应急预案"
        }
    ]

    return json.dumps(list)


application = app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888, debug=True)