#coding:utf-8
from flask import Flask,request,render_template
import mysql.connector
import os

import json

conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='shenzhen_event',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/img",methods=["POST"])
def test():
    try:
        img = request.files.get("images")
        path = basedir + "/static/file/"
        file_path = path + img.filename
        img.save(file_path)
        location = "http://183.66.213.82:8888/tushifang/static/file/"+ img.filename
        return location
    except Exception,err:
        return str(err)



# 向数据库中写入数据
@app.route("/insert",methods=["POST"])
def insert():

    data = request.get_json()

    # 基本信息
    date = data["date"]         # 当天日期          date
    start_date = data["start_date"]    # 工期开始时间(默认值)     date
    end_date = data["end_date"]     # 工期结束时间(默认值)       date
    days = data["days"]     # 工期 (=计划结束日期-计划开始日期)       date
    days_gone = data["days_gone"]       # 已用工期(=日期-工期开始日期)      int
    days_remain = data["days_remain"]       # 剩余工期(工期-已用工期)         int
    out_total = data["out_total"]       # 总土石方量 (默认值)       int
    plan_out = data["plan_out"]     # 计划每日出土方量(=总土石方量/土石方工期)        float
    plan_car = data["plan_car"]     # 计划每日出土车数 (=计划每日出土方量/运渣车核载量（方))        int
    day_out_total = data["day_out_total"]       # 累计出土方量 (后端给数据)        float

    # 每日详情
    car_take = data["car_take"]         # 运渣车核载量（方)   (需要输入)        float
    car_amount = data["car_amount"]         # 运渣车数量     (需要输入)      int
    zhachang = data["zhachang"]         # 渣场    (需要输入)      str
    distance = data["distance"]         # 运距    (需要输入)      float
    digger_amount = data["digger_amount"]           # 挖机数量  (需要输入)      int
    day_car_out = data["day_car_out"]       # 当日出土车数    (需要输入)      int
    day_out = data["day_out"]           # 当日出土方量    (需要输入)      float

    # 渣票
    manager = data["manager"]           # 施工单位经办人       str

    # 进度情况
    plan_day_out = data["plan_day_out"]         # 计划累计出土方(=计划每日出土方量*已用工期)       float
    deviation_out = data["deviation_out"]          # 出土方偏差(=实际累计出土方量-计划累计出土方量)      float
    out_remain = data["out_remain"]         # 实际剩余土石方(=总土石方量-实际累计出土方量)      float
    plan_out_remain = data["plan_out_remain"]           # 计划剩余土石方(=总土石方量-计划累计出土方量)      float
    deviation_remain = data["deviation_remain"]         # 剩余土石方偏差(=实际剩余土石方量-计划剩余土石方量)       float
    car_amount_total = data["car_amount_total"]         # 实际累计出土车数 (后端给数据)      int
    car_amount_plan = data["car_amount_plan"]           #计划累计出土车数(=计划每日出土车数*已用工期)     int
    deviation_car_amount = data["deviation_car_amount"]         # 出土车数偏差(=实际累计出土车数-计划累计出土车数)        int
    rate = data["rate"]         # 实际完成比例(=实际累计出土方量/总土石方量)        float
    plan_rate = data["plan_rate"]           # 计划完成比例(=计划累计出土方量/总土石方量)        float
    deviation_rate = data["deviation_rate"]         # 比例偏差(=实际完成比例-计划完成比例)    float

    # 调整建议
    advice_out = data["advice_out"]         # 后续每日建议出土方量(=实际剩余土石方量/剩余工期)        float
    advice_car = data["advice_car"]         # 后续每日建议出土车数(=实际剩余土石方量/剩余工期/核载量)        int


    # 渣票(图片)
    file_path = data["file_path"]


    insert = "insert into yuelai__tushifang (date,start_date,end_date,days,days_gone,days_remain,out_total,plan_out,plan_car,day_out_total,car_take,car_amount,zhachang,distance,digger_amount,day_car_out,day_out,manager,plan_day_out,deviation_out,out_remain,plan_out_remain,deviation_remain,car_amount_total,car_amount_plan,deviation_car_amount,rate,plan_rate,deviation_rate,advice_out,advice_car,file_path) values (%s,%s,%s,%d,%d,%d,%d,%f,%d,%f,%f,%d,%s,%f,%d,%d,%f,%s,%f,%f,%f,%f,%f,%d,%d,%d,%f,%f,%f,%f,%d,%s)"%("'"+date+"'","'"+start_date+"'","'"+end_date+"'",days,days_gone,days_remain,out_total,plan_out,plan_car,day_out_total,car_take,car_amount,"'"+zhachang+"'",distance,digger_amount,day_car_out,day_out,"'"+manager+"'",plan_day_out,deviation_out,out_remain,plan_out_remain,deviation_remain,car_amount_total,car_amount_plan,deviation_car_amount,rate,plan_rate,deviation_rate,advice_out,advice_car,"'"+file_path+"'")

    cursor.execute(insert)
    conn.commit()


    return "data inserted"

# 查看表格  只需要Post日期
@app.route("/select",methods=["POST"])
def select():
    data = request.get_json()
    page = data["page"]

    # 数据库操作
    search = "select * from yuelai__tushifang limit "+str((page-1)*10)+",10"
    cursor.execute(search)
    info = cursor.fetchall()

    # 数据整理
    list = []
    for i in info:


        dict={
        "date" : i[1].strftime('%Y-%m-%d'),
        "start_date" : i[2].strftime('%Y-%m-%d'),
        "end_date" : i[3].strftime('%Y-%m-%d'),
        "days" : i[4],
        "days_gone" : i[5],
        "days_remain" : i[6],
        "out_total" : i[7],
        "plan_out" : i[8],
        "plan_car" : i[9],
        "day_out_total" : i[10],
        # 每日详情
        "car_take" : i[11],
        "car_amount" : i[12],
        "zhachang" : i[13],
        "distance" : i[14],
        "digger_amount" : i[15],
        "day_car_out" : i[16],
        "day_out" : i[17],
        # 渣票
        "manager" : i[18],
        # 进度情况
        "plan_day_out" : i[19],
        "deviation_out" : i[20],
        "out_remain" : i[21],
        "plan_out_remain" : i[22],
        "deviation_remain" : i[23],
        "car_amount_total" : i[24],
        "car_amount_plan" : i[25],
        "deviation_car_amount" : i[26],
        "rate": i[27],
        "plan_rate": i[28],
        "deviation_rate":i[29],
        # 调整建议
        "advice_out" :i[30],
        "advice_car" :i[31],
        "file_path":i[32]
        }

        list.append(dict)

    return json.dumps(list)

# 页数
@app.route("/page")
def page():

    # 数据库操作
    search = "select * from yuelai__tushifang"
    cursor.execute(search)
    info = cursor.fetchall()

    return json.dumps(len(info))

# 累计数据调取接口:

# 累计出土方量
@app.route('/day_out_total')
def day_out_total():

    # 数据库操作
    search = "select day_out from yuelai__tushifang"
    cursor.execute(search)
    result = cursor.fetchall()

    #逻辑判断, 结果相加
    sum = 0
    for data in result:
        if data == "null":
            data = 0
        else:
            data = data[0]

        sum = sum + data

    day_out_total = [{"day_out_total":sum}]

    return json.dumps(day_out_total)

# 实际累计出土车数
@app.route('/car_amount_total')
def car_amount_total():

    # 数据库操作
    search = "select day_car_out from yuelai__tushifang"
    cursor.execute(search)
    result = cursor.fetchall()

    #逻辑判断, 结果相加
    sum = 0
    for data in result:
        if data == "null":
            data = 0
        else:
            data = data[0]

        sum = sum + data



    car_amount_total = [{"car_amount_total":sum}]

    return json.dumps(car_amount_total)


application = app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)
