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

canlian = Blueprint('canlian', __name__)

# 重庆市残疾人康复中心项目大屏


# 驾驶舱
# @canlian.route("/")
# def index():
#     return render_template("index_canlian.html")

# 项目概况
@canlian.route("/index/intro")
def canlian_intro():
    dict = {"data":{
        "data": """        重庆市残疾人康复中心 （一期）工程位于大渡口区大渡口组团H分区H15-15-3号宗地。项目投资：项目总投资16992.04万元。其中工程费14111.53万元，工程建设其他费2071.36万元，预备费809.15万元。资金来源：中央预算内投资3200万元，市预算内统筹资金1000万元，市残疾人就业保障金12793万元。
        本项目总用地面积31587平方米，建筑密度12.74%，容积率0.662，绿地率38.89%。拟建总建筑面积为30394.41平方米，其中地上建筑面积20907.12平方米，地下建筑面积9487.29平方米。停车位254个（其中地上车位76个，地下车位178个）。项目主要建设内容包括2栋建筑（1#楼，2#楼）。1#楼主要包括：餐厅、影像检验、信息中心、辅具用房、听力康复业务用房、管理用房；2#楼主要包括：康复门诊、社区医疗、康复理疗业务用房；地下建筑包括：车库、设备用房、医疗辅助用房。
        """
    }}
    return json.dumps(dict)

# 效果图预览
@canlian.route("/index/pic")
def canlian_pic():
    list={
       "data":{"data":[{"url":"http://183.66.213.82:8888/screen/static/canlian_pic/1.jpg"},{"url":"http://183.66.213.82:8888/screen/static/canlian_pic/2.jpg"},{"url":"http://183.66.213.82:8888/screen/static/canlian_pic/3.jpg"},{"url":"http://183.66.213.82:8888/screen/static/canlian_pic/4.jpg"},{"url":"http://183.66.213.82:8888/screen/static/canlian_pic/5.jpg"},{"url":"http://183.66.213.82:8888/screen/static/canlian_pic/6.jpg"},{"url":"http://183.66.213.82:8888/screen/static/canlian_pic/7.jpg"}]}
    }
    return json.dumps(list)

# 参建单位
@canlian.route("/index/company")
def canlian_company():
    list = {"data":[
        {
            "unit": "建设单位",
            "company": "重庆市残疾人联合会"
        },
        {
            "unit": "项目管理+BIM单位",
            "company": "林同棪国际工程咨询（中国）有限公司"
        }, {
            "unit": "设计单位",
            "company": "中煤科工集团重庆设计研究院有限公司"
        }, {
            "unit": "勘察单位",
            "company": "深圳市工勘岩土集团有限公司"
        }, {
            "unit": "施工单位",
            "company": "重庆建工住房建设有限公司"
        }, {
            "unit": "监理单位",
            "company": "河南新恒丰工程咨询有限公司"
        }, {
            "unit": "财务审计单位",
            "company": "重庆渝证会计师事务所有限公司"
        },{
            "unit": "造价审计单位",
            "company": "重庆恒诺建设工程咨询有限公司"
        }
    ]}
    return json.dumps(list)

# 进度
@canlian.route("/index/jindu")
def canlian_jindu():

    list = [
        {"data": 5,
         "name":"土建工程"},
        {"data":0,
         "name":"机电工程"},
        {"data":0,
         "name":"精装工程"},
        {"data": 0,
         "name":"室外工程"},
    ]
    return json.dumps(list)

# 无人机地址
@canlian.route("/index/wurenji")
def canlian_wurenji():
    dict = {"data":
        {"data":"https://720yun.com/t/7fvknefq0pl"}
    }
    return json.dumps(dict)

# 模型(左)地址
@canlian.route("/index/iframe_left")
def canlian_iframe_left():
    dict = {"data":
        {"data":"http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=JjEBzi"}
    }
    return json.dumps(dict)

# 模型(右)地址
@canlian.route("/index/iframe_right")
def canlian_iframe_right():
    dict = {"data":
        {"data":"http://www.tylinbim.com/4DAnalog/qrshare/s.action?newUrl=Nfe2e2"}
    }
    return json.dumps(dict)

# 产值统计
@canlian.route("/index/chanzhi")
def canlian_index_renyuan():
    dict = {
        "x":["2019.5","2019.6","2019.7","2019.8","2019.8","2019.10"],
        "y":[{"name":"计划产值","data":[347.1573,11.5737,195.98072,193.561038,180.201926,189.676911]},{"name":"实际产值","data":[347.1573,11.5737,195.98072,193.561038,180.201926,189.676911]}]
    }
    return json.dumps(dict)

# 质量&安全问题
@canlian.route("/index/zhiliang_anquan")
def canlian_index_safe():
    # 安全部分

    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/safety.action"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]


    list_safe = []
    for i in dataList_1:
        if i["rectificate"] == "是":
            list_safe.append(i)

    # 质量部分

    url_2 = "http://www.tylinbim.com/4DAnalog/ltyCL/quality.action"
    res_2 = requests.get(url_2)
    data_2 = json.loads(res_2.text)
    dataList_2 = data_2["data"]

    list_quality = []
    for j in dataList_2:
        if j["rectificate"] == "是":
            list_quality.append(j)

    y = [
        {"name":"问题总数","data": [len(dataList_1),len(dataList_2)]},
        {"name":"已解决","data": [len(list_safe),len(list_quality)]}
    ]
    x = ["安全问题","质量问题"]

    dict = {"y": y, "x": x}

    return json.dumps(dict)

# 天气
@canlian.route("/index/weather")
def canlian_index_weather():
    # 数据库查询
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                               database='canlian_data',
                                               auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()
    sql_weather = "select pm2p5,pm10,noise,temperature from environment order by id desc LIMIT 1"
    cursor.execute(sql_weather)
    enviroment = cursor.fetchall()
    conn.close()
    # 获取剩余天数
    days = requests.get("http://183.66.213.82:8888/shenzhen/date/begin?d=2019-06-30")
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

# 天气接口
@canlian.route('/data_environment',methods=['POST'])
def canlian_data_environment():
    data = request.get_json()
    deviceSerial = data["deviceSerial"]
    recordtime = data["recordtime"]
    temperature = float(data["temperature"])
    humidity = float(data["humidity"])
    pm2p5 = float(data["pm2p5"])
    pm10 = float(data["pm10"])
    noise = float(data["noise"])
    windspeed = float(data["Windspeed"])
    winddirection = float(data["winddirection"])

    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
    cursor = conn.cursor()

    sql = "insert into environment (deviceSerial,recordtime,temperature,humidity,pm2p5,pm10,noise,windspeed,winddirection) values(%s,%s,%f,%f,%f,%f,%f,%f,%f)" % ("'" + deviceSerial + "'", "'" + recordtime + "'", temperature, humidity, pm2p5, pm10, noise, windspeed,winddirection)
    cursor.execute(sql)
    conn.commit()
    conn.close()

    return "已收到数据"

# 人员接口
@canlian.route('/data_person',methods=['POST'])
def canlian_data_person():
    data = request.get_json()
    personName = data["personName"]
    positionName = data["positionName"]
    inOut = int(data["inOut"])
    companyName = data["companyName"]
    pictureUrl = data["pictureUrl"]
    accessTime = data["accessTime"]

    try:
        conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
        cursor = conn.cursor()
        sql = "insert into access (personName,positionName,inOrout,companyName,pictureUrl,accessTime) values(%s,%s,%d,%s,%s,%s)"%("'"+personName+"'","'"+positionName+"'",inOut,"'"+companyName+"'","'"+pictureUrl+"'","'"+accessTime+"'")
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return json.dumps({"code":200,"msg":"已收到数据"})
    except Exception as e:
        return json.dumps({"code":500,"msg":e})




# 质量安全接口
# 质量管理
# 饼状图
@canlian.route("/quality/circle")
def canlian_quality_circle():

    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/quality.action"
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

# 本周质量问题统计
@canlian.route("/quality/week_question_state")
def canlian_quality_week_question_state():
    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/quality.action"
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

# 累计质量问题统计
@canlian.route("/quality/week_question")
def canlian_quality_week_question():
    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/quality.action"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    datetime_now = datetime.datetime.now()
    today = datetime_now.strftime("%Y-%m")
    last_1_day = (datetime_now - relativedelta(months=1)).strftime("%Y-%m")
    last_2_day = (datetime_now - relativedelta(months=2)).strftime("%Y-%m")
    last_3_day = (datetime_now - relativedelta(months=3)).strftime("%Y-%m")
    last_4_day = (datetime_now - relativedelta(months=4)).strftime("%Y-%m")
    last_5_day = (datetime_now - relativedelta(months=5)).strftime("%Y-%m")
    last_6_day = (datetime_now - relativedelta(months=6)).strftime("%Y-%m")

    today_list = []
    last_1_day_list = []
    last_2_day_list = []
    last_3_day_list = []
    last_4_day_list = []
    last_5_day_list = []
    last_6_day_list = []
    last_list=[]

    today_solved_list = []
    last_1_day_solved_list = []
    last_2_day_solved_list = []
    last_3_day_solved_list = []
    last_4_day_solved_list = []
    last_5_day_solved_list = []
    last_6_day_solved_list = []
    last_solved_list=[]

    for i in dataList_1:
        if i["checkTime"][:-3] == today:
            today_list.append(i)
            if i["rectificate"] == "是":
                today_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_1_day:
            last_1_day_list.append(i)
            if i["rectificate"] == "是":
                last_1_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_2_day:
            last_2_day_list.append(i)
            if i["rectificate"] == "是":
                last_2_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_3_day:
            last_3_day_list.append(i)
            if i["rectificate"] == "是":
                last_3_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_4_day:
            last_4_day_list.append(i)
            if i["rectificate"] == "是":
                last_4_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_5_day:
            last_5_day_list.append(i)
            if i["rectificate"] == "是":
                last_5_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_6_day:
            last_6_day_list.append(i)
            if i["rectificate"] == "是":
                last_6_day_solved_list.append(i)
            else:
                pass
        else:
            last_list.append(i)
            if i["rectificate"] == "是":
                last_solved_list.append(i)
            else:
                pass

    m1 = (datetime_now - relativedelta(months=6)).strftime("%Y-%m")
    m2 = (datetime_now - relativedelta(months=5)).strftime("%Y-%m")
    m3 = (datetime_now - relativedelta(months=4)).strftime("%Y-%m")
    m4 = (datetime_now - relativedelta(months=3)).strftime("%Y-%m")
    m5 = (datetime_now - relativedelta(months=2)).strftime("%Y-%m")
    m6 = (datetime_now - relativedelta(months=1)).strftime("%Y-%m")
    m7 = datetime_now.strftime("%Y-%m")

    dict = {
        "data": {
            "x": [m1, m2, m3, m4, m5, m6, m7],
            "total": [len(last_6_day_list)+len(last_list), len(last_5_day_list)+len(last_6_day_list)+len(last_list), len(last_4_day_list)+len(last_5_day_list)+len(last_6_day_list)+len(last_list), len(last_3_day_list)+len(last_4_day_list)+len(last_5_day_list)+len(last_6_day_list)+len(last_list),
                      len(last_2_day_list)+len(last_3_day_list)+len(last_4_day_list)+len(last_5_day_list)+len(last_6_day_list)+len(last_list), len(last_1_day_list)+len(last_2_day_list)+len(last_3_day_list)+len(last_4_day_list)+len(last_5_day_list)+len(last_6_day_list)+len(last_list), len(today_list)+len(last_1_day_list)+len(last_2_day_list)+len(last_3_day_list)+len(last_4_day_list)+len(last_5_day_list)+len(last_6_day_list)+len(last_list)],
            "solved": [len(last_6_day_solved_list)+len(last_solved_list), len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list), len(last_4_day_solved_list)+len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list),
                       len(last_3_day_solved_list)+len(last_4_day_solved_list)+len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list), len(last_2_day_solved_list)+len(last_3_day_solved_list)+len(last_4_day_solved_list)+len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list), len(last_1_day_solved_list)+len(last_2_day_solved_list)+len(last_3_day_solved_list)+len(last_4_day_solved_list)+len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list),
                       len(today_solved_list)+len(last_1_day_solved_list)+len(last_2_day_solved_list)+len(last_3_day_solved_list)+len(last_4_day_solved_list)+len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list)]}
    }
    return json.dumps(dict)

# 累计施工质量问题对比
@canlian.route("/quality/team")
def canlian_quality_team():

    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/quality.action"
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

# 本周质量问题定位
@canlian.route("/quality/location")
def canlian_qulity_location():
    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/quality.action"
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

    weeklist = today_list + last_1_day_list + last_2_day_list + last_3_day_list + last_4_day_list + last_5_day_list + last_6_day_list
    x_list=[]
    for j in weeklist:
        if j["subDivision"] == "":
            j["subDivision"] = "未分组"
        x_list.append(j["subDivision"])
    x_list = list(set(x_list))
    y_list = []
    y_finiallist =[]
    for mm in x_list:
        for nn in weeklist:
            if nn["subDivision"] == mm:
                y_list.append(mm)
    for k in x_list:
        y_finiallist.append(y_list.count(k))

    return json.dumps({"data":{"x":x_list,"y":y_finiallist}})


# 安全管理
# 饼状图
@canlian.route("/safe/circle")
def canlian_safe_circle():

    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/safety.action"
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

# 本周安全问题统计
@canlian.route("/safe/week_question_state")
def canlian_safe_week_question_state():
    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/safety.action"
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

# 累计安全问题统计
@canlian.route("/safe/week_question")
def canlian_safe_week_question():
    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/safety.action"
    res_1 = requests.get(url_1)
    data_1 = json.loads(res_1.text)
    dataList_1 = data_1["data"]

    datetime_now = datetime.datetime.now()
    today = datetime_now.strftime("%Y-%m")
    last_1_day = (datetime_now - relativedelta(months=1)).strftime("%Y-%m")
    last_2_day = (datetime_now - relativedelta(months=2)).strftime("%Y-%m")
    last_3_day = (datetime_now - relativedelta(months=3)).strftime("%Y-%m")
    last_4_day = (datetime_now - relativedelta(months=4)).strftime("%Y-%m")
    last_5_day = (datetime_now - relativedelta(months=5)).strftime("%Y-%m")
    last_6_day = (datetime_now - relativedelta(months=6)).strftime("%Y-%m")

    today_list = []
    last_1_day_list = []
    last_2_day_list = []
    last_3_day_list = []
    last_4_day_list = []
    last_5_day_list = []
    last_6_day_list = []
    last_list=[]

    today_solved_list = []
    last_1_day_solved_list = []
    last_2_day_solved_list = []
    last_3_day_solved_list = []
    last_4_day_solved_list = []
    last_5_day_solved_list = []
    last_6_day_solved_list = []
    last_solved_list=[]

    for i in dataList_1:
        if i["checkTime"][:-3] == today:
            today_list.append(i)
            if i["rectificate"] == "是":
                today_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_1_day:
            last_1_day_list.append(i)
            if i["rectificate"] == "是":
                last_1_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_2_day:
            last_2_day_list.append(i)
            if i["rectificate"] == "是":
                last_2_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_3_day:
            last_3_day_list.append(i)
            if i["rectificate"] == "是":
                last_3_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_4_day:
            last_4_day_list.append(i)
            if i["rectificate"] == "是":
                last_4_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_5_day:
            last_5_day_list.append(i)
            if i["rectificate"] == "是":
                last_5_day_solved_list.append(i)
            else:
                pass
        elif i["checkTime"][:-3] == last_6_day:
            last_6_day_list.append(i)
            if i["rectificate"] == "是":
                last_6_day_solved_list.append(i)
            else:
                pass
        else:
            last_list.append(i)
            if i["rectificate"] == "是":
                last_solved_list.append(i)
            else:
                pass

    m1 = (datetime_now - relativedelta(months=6)).strftime("%Y-%m")
    m2 = (datetime_now - relativedelta(months=5)).strftime("%Y-%m")
    m3 = (datetime_now - relativedelta(months=4)).strftime("%Y-%m")
    m4 = (datetime_now - relativedelta(months=3)).strftime("%Y-%m")
    m5 = (datetime_now - relativedelta(months=2)).strftime("%Y-%m")
    m6 = (datetime_now - relativedelta(months=1)).strftime("%Y-%m")
    m7 = datetime_now.strftime("%Y-%m")

    dict = {
        "data": {
            "x": [m1, m2, m3, m4, m5, m6, m7],
            "total": [len(last_6_day_list)+len(last_list), len(last_5_day_list)+len(last_6_day_list)+len(last_list), len(last_4_day_list)+len(last_5_day_list)+len(last_6_day_list)+len(last_list), len(last_3_day_list)+len(last_4_day_list)+len(last_5_day_list)+len(last_6_day_list)+len(last_list),
                      len(last_2_day_list)+len(last_3_day_list)+len(last_4_day_list)+len(last_5_day_list)+len(last_6_day_list)+len(last_list), len(last_1_day_list)+len(last_2_day_list)+len(last_3_day_list)+len(last_4_day_list)+len(last_5_day_list)+len(last_6_day_list)+len(last_list), len(today_list)+len(last_1_day_list)+len(last_2_day_list)+len(last_3_day_list)+len(last_4_day_list)+len(last_5_day_list)+len(last_6_day_list)+len(last_list)],
            "solved": [len(last_6_day_solved_list)+len(last_solved_list), len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list), len(last_4_day_solved_list)+len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list),
                       len(last_3_day_solved_list)+len(last_4_day_solved_list)+len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list), len(last_2_day_solved_list)+len(last_3_day_solved_list)+len(last_4_day_solved_list)+len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list), len(last_1_day_solved_list)+len(last_2_day_solved_list)+len(last_3_day_solved_list)+len(last_4_day_solved_list)+len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list),
                       len(today_solved_list)+len(last_1_day_solved_list)+len(last_2_day_solved_list)+len(last_3_day_solved_list)+len(last_4_day_solved_list)+len(last_5_day_solved_list)+len(last_6_day_solved_list)+len(last_solved_list)]}
    }
    return json.dumps(dict)

# 累计施工安全问题对比
@canlian.route("/safe/team")
def canlian_safe_team():

    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/safety.action"
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

# 本周安全问题定位
@canlian.route("/safe/location")
def canlian_safe_location():
    url_1 = "http://www.tylinbim.com/4DAnalog/ltyCL/safety.action"
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

    weeklist = today_list + last_1_day_list + last_2_day_list + last_3_day_list + last_4_day_list + last_5_day_list + last_6_day_list
    x_list=[]
    for j in weeklist:
        if j["subDivision"] == "":
            j["subDivision"] = "未分组"
        x_list.append(j["subDivision"])
    x_list = list(set(x_list))
    y_list = []
    y_finiallist =[ ]
    for mm in x_list:
        for nn in weeklist:
            if nn["subDivision"] == mm:
                y_list.append(mm)
    for k in x_list:
        y_finiallist.append(y_list.count(k))

    return json.dumps({"data":{"x":x_list,"y":y_finiallist}})


# 环境监测接口
# 风速
# 圆环(当前)
@canlian.route("/environment/wind_now")
def wind_now():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/wind_high")
def wind_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/wind_echart")
def wind_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/humidity_now")
def humidity_now():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/humidity_high")
def humidity_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/humidity_echart")
def humidity_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/temperature_now")
def temperature_now():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/temperature_high")
def temperature_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/temperature_echart")
def temperature_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/noise_now")
def noise_now():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/noise_high")
def noise_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/noise_echart")
def noise_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/pm2p5_average")
def pm2p5_average():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/pm2p5_echart")
def pm2p5_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/pm2p5_high")
def pm2p5_high():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/pm10_average")
def pm10_average():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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
@canlian.route("/environment/pm10_echart")
def pm10_echart():
    conn = mysql.connector.connect(host='183.66.213.82', port="8803", user='tylin', password='Tylin@123',
                                   database='canlian_data', auth_plugin='mysql_native_password')  # 连接数据库，创建Flask_app数据库
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


# 监控视频
@canlian.route("/cam")
def cam():
    dict={"data":[{"url":"http://113.204.233.198:7086/live/cameraid/1000295%240/substream/1.m3u8","name":"残疾人康复中心大门"},{"url":"http://113.204.233.198:7086/live/cameraid/1000295%241/substream/1.m3u8","name":"残疾人康复中心生活区"}]}
    return json.dumps(dict)