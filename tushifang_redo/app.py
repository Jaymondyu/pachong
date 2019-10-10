#coding:utf-8
from flask import Flask,request,render_template
import mysql.connector
import datetime
import os
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='shenzhen_event',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/show")
def show():
    return render_template("show.html")
@app.route("/down")
def down():
    return render_template("down.html")
@app.route("/data")
def data():
    return render_template("data.html")

# 上传渣票打包文件
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

# 默认值设定
start_date = datetime.datetime.strptime("2019-7-10",'%Y-%m-%d')      # 工期开始时间(默认值)
end_date = datetime.datetime.strptime("2019-12-25",'%Y-%m-%d')       # 工期结束时间(默认值)
days = int(str(end_date - start_date).replace("days, 0:00:00",""))         # 工期 (=计划结束日期-计划开始日期
out_total = 634000           # 总土石方量 (默认值)
plan_out = out_total / days         # 计划每日出土方量(=总土石方量/土石方工期
car_take = 18               #核载量
plan_car = plan_out / car_take  # 计划每日出土车数 (=计划每日出土方量/运渣车核载量（方))

# 累计出土方量调取方法
def leiji(date):
    search = "select day_out from yuelai__tushifang where date <" + "'" + str(date) + "'"
    cursor.execute(search)
    result = cursor.fetchall()
    sum = 0
    for i in result:
        sum = sum + i[0]
    return sum

# 实际累计出土车数
def leiji_che(date):
    search = "select day_car_out from yuelai__tushifang where date <" + "'" + str(date) + "'"
    cursor.execute(search)
    result = cursor.fetchall()
    sum = 0
    for i in result:
        sum = sum + i[0]
    return sum


# 向数据库中写入数据
@app.route("/insert",methods=["POST"])
def insert():

    # 获取前端传来的信息-----------------------------------------------------------------------------------------------------------------------------
    data = request.get_json()

    # 基本信息
    date = datetime.datetime.strptime(data["date"],'%Y-%m-%d')        # 当天日期          date
    car_amount = data["car_amount"]         # 运渣车数量     (需要输入)      int
    zhachang = data["zhachang"]         # 渣场    (需要输入)      str
    distance = data["distance"]         # 运距    (需要输入)      float
    digger_amount = data["digger_amount"]           # 挖机数量  (需要输入)      int
    day_car_out = data["day_car_out"]       # 当日出土车数    (需要输入)      int
    day_out = data["day_out"]           # 当日出土方量    (需要输入)      float
    manager = data["manager"]           # 施工单位经办人       str
    area = data["area"]                 # 区域       str
    ps = data["ps"]                     # 备注       str
    file_path = data["file_path"]       # 渣票(压缩包地址)        str

    # 开始计算 --------------------------------------------------------------------------------------------------------------------------------------

    # 进度情况
    days_gone = str(date - start_date)         # 已用工期(=日期-工期开始日期)
    if days_gone == "0:00:00":
        days_gone = 0
    elif days_gone == "1 day, 0:00:00":
        days_gone = 1
    else:
        days_gone = int(str(date - start_date).replace(" days, 0:00:00",""))
    days_remain = days - days_gone          # 剩余工期(工期-已用工期)
    day_out_total = leiji(date) + day_out        # 累计出土方量
    plan_day_out = plan_out * days_gone           # 计划累计出土方(=计划每日出土方量*已用工期)
    deviation_out = day_out_total - plan_day_out        # 出土方偏差(=实际累计出土方量-计划累计出土方量)
    out_remain = out_total - day_out_total                 # 实际剩余土石方(=总土石方量-实际累计出土方量)
    plan_out_remain = out_total - plan_day_out          # 计划剩余土石方(=总土石方量-计划累计出土方量)
    deviation_remain = out_remain - plan_out_remain         # 剩余土石方偏差(=实际剩余土石方量-计划剩余土石方量)
    car_amount_total = leiji_che(date) + day_car_out        # 实际累计出土车数
    car_amount_plan = plan_car * days_gone                  #计划累计出土车数(=计划每日出土车数*已用工期
    deviation_car_amount = car_amount_total - car_amount_plan                # 出土车数偏差(=实际累计出土车数-计划累计出土车数)
    rate = (day_out_total/float(out_total))*100                   # 实际完成比例(=实际累计出土方量/总土石方量)
    plan_rate = (plan_day_out/float(out_total))*100               # 计划完成比例(=计划累计出土方量/总土石方量)
    deviation_rate = rate - plan_rate                # 比例偏差(=实际完成比例-计划完成比例)

    # 调整建议
    advice_out = out_remain/days_remain               # 后续每日建议出土方量(=实际剩余土石方量/剩余工期)
    advice_car = advice_out/car_take                # 后续每日建议出土车数(=实际剩余土石方量/剩余工期/核载量)


    # 录入数据库 --------------------------------------------------------------------------------------------------------------------------------------------------
    insert = """insert into yuelai__tushifang
    (date,start_date,end_date,days,days_gone,days_remain,out_total,plan_out,plan_car,day_out_total,car_take,car_amount,zhachang,distance,digger_amount,day_car_out,day_out,manager,plan_day_out,deviation_out,out_remain,plan_out_remain,deviation_remain,car_amount_total,car_amount_plan,deviation_car_amount,rate,plan_rate,deviation_rate,advice_out,advice_car,file_path,area,ps)
    values
    (%s,%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%s,%d,%d,%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%s,%s)"""%("'"+str(date)+"'","'"+str(start_date)+"'","'"+str(end_date)+"'",days,days_gone,days_remain,out_total,plan_out,plan_car,day_out_total,car_take,car_amount,"'"+zhachang+"'","'"+str(distance)+"'",digger_amount,day_car_out,day_out,"'"+manager+"'",plan_day_out,deviation_out,out_remain,plan_out_remain,deviation_remain,car_amount_total,car_amount_plan,deviation_car_amount,rate,plan_rate,deviation_rate,advice_out,advice_car,"'"+file_path+"'","'"+ps+"'","'"+area+"'")

    cursor.execute(insert)
    conn.commit()



    return "data inserted"

# 查看表格  只需要Post日期
@app.route("/select",methods=["POST"])
def select():
    data = request.get_json()
    page = data["page"]

    # 数据库操作
    search = "select * from yuelai__tushifang order by date desc limit "+str((page-1)*10)+",10"
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
        "file_path":i[32],
        "area":i[34],
        "ps":i[33]
        }

        list.append(dict)

    return json.dumps(list)

#最近一个查询
@app.route("/last")
def last():
    # 数据库操作
    search = "select * from yuelai__tushifang order by date desc limit 1"
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
        "file_path":i[32],
        "area":i[33],
        "ps":i[34]
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

# ---------------------------------------------------华丽分割线-------------------------------------------------------------------
# ---------------------------------------------------华丽分割线-------------------------------------------------------------------
# ---------------------------------------------------华丽分割线-------------------------------------------------------------------
# ---------------------------------------------------华丽分割线-------------------------------------------------------------------

# 土石方图表页

# 累计出土方量计划值与实际值对比
@app.route("/real_vs_plan/total")
def r_vs_p_total():
    # 数据库操作
    search = "select date,day_out_total,plan_day_out from yuelai__tushifang order by date"
    cursor.execute(search)
    info = cursor.fetchall()

    x = []
    real =[]
    plan=[]

    for i in info:
        x.append(i[0].strftime('%Y-%m-%d'))
        real.append(i[1])
        plan.append(i[2])

    dict = {
        "data":{
            "x":x,
            "real":real,
            "plan":plan
        }
    }

    return json.dumps(dict)

# 每日出土方量计划值与实际值对比
@app.route("/real_vs_plan/day")
def r_vs_p_day():
    # 数据库操作
    search = "select date,day_out,plan_out,advice_out from yuelai__tushifang order by date"
    cursor.execute(search)
    info = cursor.fetchall()

    x = []
    real =[]
    plan=[]
    advice=[0]

    for i in info:
        x.append(i[0].strftime('%Y-%m-%d'))
        real.append(i[1])
        plan.append(i[2])
        advice.append(i[3])

    dict = {
        "data":{
            "x":x,
            "real":real,
            "plan":plan,
            "advice":advice[:-1]
        }
    }

    return json.dumps(dict)

# 环形 & 扇形 图表
# 1. 实际累计出土方量 vs 计划累计出土方量(环)
@app.route("/circle/real_vs_plan")
def circle_r_vs_p():
    # 数据库操作
    search = "select date,day_out_total,plan_day_out from yuelai__tushifang order by date desc limit 1"
    cursor.execute(search)
    info = cursor.fetchall()

    real =[]
    plan=[]

    for i in info:
        real.append(i[1])
        plan.append(i[2])

    left_real = out_total-real[0]
    left_plan = out_total-plan[0]

    dict = {
        "data":{
            "real":real,
            "plan":plan,
            "left_real":left_real,
            "left_plan":left_plan
        }
    }

    return json.dumps(dict)
# 2. 实际累计出土方量占比 vs 已用工期占比(环)
@app.route("/circle/rate_vs_daysrate")
def circle_rate_vs_daysrate():
    # 数据库操作
    search = "select day_out_total,days,days_gone from yuelai__tushifang order by date desc limit 1"
    cursor.execute(search)
    info = cursor.fetchall()

    rate = []
    daysrate = []
    for i in info:
        rate.append(i[0]/float(out_total)*100)
        daysrate.append((i[2]/float(i[1]))*100)
    dict = {
        "data":{
            "rate":rate,
            "daysrate":daysrate,
            "left_rate":100-rate[0],
            "left_daysrate":100-daysrate[0]
        }
    }


    return json.dumps(dict)
# 3. 实际累计出土方量 vs 实际剩余土石方量(饼)
@app.route("/pie/out_vs_remain")
def pie_out_vs_remain():
    # 数据库操作
    search = "select day_out_total,out_remain from yuelai__tushifang order by date desc limit 1"
    cursor.execute(search)
    info = cursor.fetchall()

    dict = {
        "data":{
            "out":info[0][0],
            "remain":info[0][1]
        }
    }

    return json.dumps(dict)
# 4. 已用工期 vs 土石方总工期
@app.route("/pie/days_vs_gone")
def pie_days_vs_gone():
    # 数据库操作
    search = "select days,days_gone from yuelai__tushifang order by date desc limit 1"
    cursor.execute(search)
    info = cursor.fetchall()

    dict = {
        "data":{
            "days":info[0][0],
            "days_gone":info[0][1]
        }
    }

    return json.dumps(dict)

# 每周数据分析图表需求说明
# 每周实际出土方量对比
@app.route("/week/out")
def week_out():
    # 数据库操作
    search = "select date,day_out from yuelai__tushifang order by date desc limit 14"
    cursor.execute(search)
    info = cursor.fetchall()

    x=[]
    y=[]
    for i in info:
        date = i[0].strftime('%a')
        x.append(date)
        y.append(i[1])

    dict = {
        "data":{
            "x":x[0:7],
            "y":y[0:7],
            "y_1":y[7:]
        }
    }

    return json.dumps(dict)
# 每周实际累计出土方量对比
@app.route("/week/out_total")
def week_out_total():
    # 数据库操作
    search = "select date,day_out_total from yuelai__tushifang order by date desc limit 14"
    cursor.execute(search)
    info = cursor.fetchall()

    x=[]
    y=[]
    for i in info:
        date = i[0].strftime('%a')
        x.append(date)
        y.append(i[1])


    dict = {
        "data":{
            "x":x[0:7],
            "y":y[0:7],
            "y_1":y[7:]
        }
    }

    return json.dumps(dict)

# 工期分析图表
# 已用vs土石方工期
@app.route("/watch/days_gone")
def watch_days_gone():
    # 数据库操作
    search = "select days_gone,days from yuelai__tushifang order by date desc limit 1"
    cursor.execute(search)
    info = cursor.fetchall()

    dict = {
        "data":{
            "days_gone":info[0][0],
            "days":info[0][1],
            "rate": (info[0][0]/float(info[0][1]))*100
        }
    }

    return json.dumps(dict)
# 已用vs总工期
@app.route("/watch/total")
def watch_total():
    # 数据库操作
    search = "select days_gone from yuelai__tushifang order by date desc limit 1"
    cursor.execute(search)
    info = cursor.fetchall()
    days=750



    dict = {
        "data":{
            "days_gone":info[0][0],
            "total":days,
            "rate": (info[0][0]/float(days))*100
        }

    }

    return json.dumps(dict)





application = app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)
