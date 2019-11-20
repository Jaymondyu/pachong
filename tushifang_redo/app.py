#coding:utf-8
from flask import Flask,request,render_template
import mysql.connector
import datetime
import os
import json
import sys
import requests
reload(sys)
sys.setdefaultencoding('utf8')

conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='shenzhen_event',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# 悦来土石方
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
    search = "select sum(day_out) from yuelai_tushifang where date <" + "'" + str(date) + "'"
    cursor.execute(search)
    result = cursor.fetchall()
    if str(result[0][0])=="None":
        result=[(0,)]


    return result[0][0]

# 实际累计出土车数
def leiji_che(date):
    search = "select sum(day_car_out) from yuelai_tushifang where date <" + "'" + str(date) + "'"
    cursor.execute(search)
    result = cursor.fetchall()
    if str(result[0][0])=="None":
        result=[(0,)]

    return result[0][0]


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
    total_price_guess = ((day_out_total)*85)/1.3        # 实际累计完成产值估算（元)= 实际累计出土方量*85/1.3
    plan_price_guess = ((plan_day_out)*85)/1.3          # 计划累计完成产值估算（元）=计划累计出土方量*85/1.3
    deviation_guess = (total_price_guess)-(plan_price_guess)        # =实际累计完成产值估算-计划累计完成产值估算
    total_guess_rate = (total_price_guess/40290026.64)*100          # 实际累计完成土石方产值占比=（实际累计完成产值/40290026.64）*100%（显示百分数）
    total_rate = (total_price_guess/597242423.14)*100               # 实际累计完成总产值占比 =（实际累计完成产值/C23）*100%（显示百分数）



    # 调整建议
    advice_out = out_remain/days_remain               # 后续每日建议出土方量(=实际剩余土石方量/剩余工期)
    advice_car = advice_out/car_take                # 后续每日建议出土车数(=实际剩余土石方量/剩余工期/核载量)


    # 录入数据库 --------------------------------------------------------------------------------------------------------------------------------------------------
    insert = """insert into yuelai_tushifang
    (date,start_date,end_date,days,days_gone,days_remain,out_total,plan_out,plan_car,day_out_total,car_take,car_amount,zhachang,distance,digger_amount,day_car_out,day_out,manager,plan_day_out,deviation_out,out_remain,plan_out_remain,deviation_remain,car_amount_total,car_amount_plan,deviation_car_amount,rate,plan_rate,deviation_rate,advice_out,advice_car,total_price_guess,plan_price_guess,deviation_guess,total_guess_rate,total_rate,file_path,area,ps)
    values
    (%s,%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%s,%d,%d,%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%f,%f,%f,%f,%f,%s,%s,%s)"""%("'"+str(date)+"'","'"+str(start_date)+"'","'"+str(end_date)+"'",days,days_gone,days_remain,out_total,plan_out,plan_car,day_out_total,car_take,car_amount,"'"+zhachang+"'","'"+str(distance)+"'",digger_amount,day_car_out,day_out,"'"+manager+"'",plan_day_out,deviation_out,out_remain,plan_out_remain,deviation_remain,car_amount_total,car_amount_plan,deviation_car_amount,rate,plan_rate,deviation_rate,advice_out,advice_car,total_price_guess,plan_price_guess,deviation_guess,total_guess_rate,total_rate,"'"+ps+"'","'"+area+"'","'"+file_path+"'")

    cursor.execute(insert)
    conn.commit()




    return "data inserted"

# 查看表格  只需要Post日期
@app.route("/select",methods=["POST"])
def select():
    data = request.get_json()
    page = data["page"]

    # 数据库操作
    search = "select * from yuelai_tushifang order by date desc limit "+str((page-1)*10)+",10"
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
        "total_price_guess":i[32],
        "plan_price_guess":i[33],
        "deviation_guess":i[34],
        "total_guess_rate":i[35],
        "total_rate":i[36],
        "file_path":i[39],
        "area":i[38],
        "ps":i[37]
        }

        list.append(dict)

    return json.dumps(list)

#最近一个查询
@app.route("/last")
def last():
    # 数据库操作
    search = "select * from yuelai_tushifang order by date desc limit 1"
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
        "total_price_guess":i[32],
        "plan_price_guess":i[33],
        "deviation_guess":i[34],
        "total_guess_rate":i[35],
        "total_rate":i[36],
        "file_path":i[39],
        "area":i[38],
        "ps":i[37]
        }

        list.append(dict)

    return json.dumps(list)

# 页数
@app.route("/page")
def page():

    # 数据库操作
    search = "select * from yuelai_tushifang"
    cursor.execute(search)
    info = cursor.fetchall()


    return json.dumps(len(info))

# ---------------------------------------------------华丽分割线-------------------------------------------------------------------
# ---------------------------------------------------华丽分割线-------------------------------------------------------------------
# ---------------------------------------------------华丽分割线-------------------------------------------------------------------
# ---------------------------------------------------华丽分割线-------------------------------------------------------------------

# 悦来土石方图表页

# 累计出土方量计划值与实际值对比
@app.route("/real_vs_plan/total")
def r_vs_p_total():
    # 数据库操作
    search = "select date,day_out_total,plan_day_out from yuelai_tushifang order by date"
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
    search = "select date,day_out,plan_out,advice_out from yuelai_tushifang order by date"
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
    search = "select date,day_out_total,plan_day_out from yuelai_tushifang order by date desc limit 1"
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
    search = "select day_out_total,days,days_gone from yuelai_tushifang order by date desc limit 1"
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
    search = "select day_out_total,out_remain from yuelai_tushifang order by date desc limit 1"
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
    search = "select days,days_gone from yuelai_tushifang order by date desc limit 1"
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
    search = "select date,day_out from yuelai_tushifang order by date desc limit 14"
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
    data = requests.get("http://183.66.213.82:8888/tushifang/week/out")
    data = data.content
    data = json.loads(data)
    x = data["data"]["x"]
    y = data["data"]["y"]
    y_1 = data["data"]["y_1"]
    y_sum=[sum(y),sum(y[1:]),sum(y[2:]),sum(y[3:]),sum(y[4:]),sum(y[5:]),sum(y[6:])]
    y_1_sum = [sum(y_1),sum(y_1[1:]),sum(y_1[2:]),sum(y_1[3:]),sum(y_1[4:]),sum(y_1[5:]),sum(y_1[6:])]
    return json.dumps({"data":{"x":x,"y_1":y_sum,"y":y_1_sum}})

# 工期分析图表
# 已用vs土石方工期
@app.route("/watch/days_gone")
def watch_days_gone():
    # 数据库操作
    search = "select days_gone,days from yuelai_tushifang order by date desc limit 1"
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
    search = "select days_gone from yuelai_tushifang order by date desc limit 1"
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

# 图片上传
@app.route("/photo",methods=["POST"])
def photo():
    try:
        img = request.files.get("photo")
        path = basedir + "/static/file/"
        file_path = path + img.filename
        img.save(file_path)
        location = "http://183.66.213.82:8888/tushifang/static/file/"+ img.filename
        sql = "insert into yuelai_tushifang_photo (url) values(%s)"%("'"+str(location)+"'")
        cursor.execute(sql)
        conn.commit()
        return "1"
    except Exception,err:
        return str(err)

# 图片展示
@app.route("/photo_show")
def photo_show():
    sql = "select url from yuelai_tushifang_photo order by id desc limit 2"
    cursor.execute(sql)
    info = cursor.fetchall()

    last = info[1][0]
    this = info[0][0]
    dict = {"last":last,
            "this":this}

    return json.dumps(dict)

# 图片上传界面
@app.route("/photo_up")
def photo_up():
    return render_template("photo.html")







# _______________________________________________________________________________________________________________________________________________________
# -------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------
# _______________________________________________________________________________________________________________________________________________________

#昆明土石方

@app.route("/kunming")
def kunming_index():
    return render_template("index_kunming.html")
@app.route("/kunming/show")
def kunming_show():
    return render_template("show_kunming.html")
@app.route("/kunming/down")
def kunming_down():
    return render_template("down_kunming.html")
@app.route("/kunming/data")
def kunming_data():
    return render_template("data_kunming.html")

# 上传渣票打包文件
@app.route("/kunming/img",methods=["POST"])
def kunming_test():
    try:
        img = request.files.get("images")
        path = basedir + "/static/file/"
        file_path = path + "kunming"+img.filename
        img.save(file_path)
        location = "http://183.66.213.82:8888/tushifang/static/file/"+ "kunming"+img.filename
        return location
    except Exception,err:
        return str(err)

# 默认值设定
kunming_start_date = datetime.datetime.strptime("2019-11-02",'%Y-%m-%d')      # 工期开始时间(默认值)
kunming_end_date = datetime.datetime.strptime("2020-02-19",'%Y-%m-%d')       # 工期结束时间(默认值)
kunming_days = 90        # 工期 (=计划结束日期-计划开始日期
kunming_out_total = 290000           # 总土石方量 (默认值)
kunming_plan_out = kunming_out_total / kunming_days         # 计划每日出土方量(=总土石方量/土石方工期
kunming_car_take = 8               #核载量
kunming_plan_car = kunming_plan_out / kunming_car_take  # 计划每日出土车数 (=计划每日出土方量/运渣车核载量（方))


# 累计出土方量调取方法
def leiji_kunming(date):
    search = "select sum(day_out) from kunming_tushifang where date <" + "'" + str(date) + "'"
    cursor.execute(search)
    result = cursor.fetchall()
    if str(result[0][0])=="None":
        result=[(0,)]


    return result[0][0]

# 实际累计出土车数
def leiji_che_kunming(date):
    search = "select sum(day_car_out) from kunming_tushifang where date <" + "'" + str(date) + "'"
    cursor.execute(search)
    result = cursor.fetchall()
    if str(result[0][0])=="None":
        result=[(0,)]

    return result[0][0]


# 向数据库中写入数据
@app.route("/kunming/insert",methods=["POST"])
def kunming_insert():

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
    days_gone = str(date - kunming_start_date)         # 已用工期(=日期-工期开始日期)
    if days_gone == "0:00:00":
        days_gone = 0
    elif days_gone == "1 day, 0:00:00":
        days_gone = 1
    else:
        days_gone = int(str(date - kunming_start_date).replace(" days, 0:00:00",""))
    days_remain = kunming_days - days_gone          # 剩余工期(工期-已用工期)
    day_out_total = leiji_kunming(date) + day_out        # 累计出土方量
    plan_day_out = kunming_plan_out * days_gone           # 计划累计出土方(=计划每日出土方量*已用工期)
    deviation_out = day_out_total - plan_day_out        # 出土方偏差(=实际累计出土方量-计划累计出土方量)
    out_remain = kunming_out_total - day_out_total                 # 实际剩余土石方(=总土石方量-实际累计出土方量)
    plan_out_remain = kunming_out_total - plan_day_out          # 计划剩余土石方(=总土石方量-计划累计出土方量)
    deviation_remain = out_remain - plan_out_remain         # 剩余土石方偏差(=实际剩余土石方量-计划剩余土石方量)
    car_amount_total = leiji_che_kunming(date) + day_car_out        # 实际累计出土车数
    car_amount_plan = kunming_plan_car * days_gone                  #计划累计出土车数(=计划每日出土车数*已用工期
    deviation_car_amount = car_amount_total - car_amount_plan                # 出土车数偏差(=实际累计出土车数-计划累计出土车数)
    rate = (day_out_total/float(kunming_out_total))*100                   # 实际完成比例(=实际累计出土方量/总土石方量)
    plan_rate = (plan_day_out/float(kunming_out_total))*100               # 计划完成比例(=计划累计出土方量/总土石方量)
    deviation_rate = rate - plan_rate                # 比例偏差(=实际完成比例-计划完成比例)
    total_price_guess = ((day_out_total)*85)/1.3        # 实际累计完成产值估算（元)= 实际累计出土方量*85/1.3
    plan_price_guess = ((plan_day_out)*85)/1.3          # 计划累计完成产值估算（元）=计划累计出土方量*85/1.3
    deviation_guess = (total_price_guess)-(plan_price_guess)        # =实际累计完成产值估算-计划累计完成产值估算
    total_guess_rate = (total_price_guess/40290026.64)*100          # 实际累计完成土石方产值占比=（实际累计完成产值/40290026.64）*100%（显示百分数）
    total_rate = (total_price_guess/597242423.14)*100               # 实际累计完成总产值占比 =（实际累计完成产值/C23）*100%（显示百分数）


    # 调整建议
    advice_out = out_remain/days_remain               # 后续每日建议出土方量(=实际剩余土石方量/剩余工期)
    advice_car = advice_out/car_take                # 后续每日建议出土车数(=实际剩余土石方量/剩余工期/核载量)


    # 录入数据库 --------------------------------------------------------------------------------------------------------------------------------------------------
    insert = """insert into kunming_tushifang
    (date,start_date,end_date,days,days_gone,days_remain,out_total,plan_out,plan_car,day_out_total,car_take,car_amount,zhachang,distance,digger_amount,day_car_out,day_out,manager,plan_day_out,deviation_out,out_remain,plan_out_remain,deviation_remain,car_amount_total,car_amount_plan,deviation_car_amount,rate,plan_rate,deviation_rate,advice_out,advice_car,total_price_guess,plan_price_guess,deviation_guess,total_guess_rate,total_rate,file_path,area,ps)
    values
    (%s,%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%s,%d,%d,%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%f,%f,%f,%f,%f,%s,%s,%s)"""%("'"+str(date)+"'","'"+str(kunming_start_date)+"'","'"+str(kunming_end_date)+"'",kunming_days,days_gone,days_remain,kunming_out_total,kunming_plan_out,kunming_plan_car,day_out_total,kunming_car_take,car_amount,"'"+zhachang+"'","'"+str(distance)+"'",digger_amount,day_car_out,day_out,"'"+manager+"'",plan_day_out,deviation_out,out_remain,plan_out_remain,deviation_remain,car_amount_total,car_amount_plan,deviation_car_amount,rate,plan_rate,deviation_rate,advice_out,advice_car,total_price_guess,plan_price_guess,deviation_guess,total_guess_rate,total_rate,"'"+ps+"'","'"+area+"'","'"+file_path+"'")

    cursor.execute(insert)
    conn.commit()




    return "data inserted"

# 查看表格  只需要Post日期
@app.route("/kunming/select",methods=["POST"])
def kunming_select():
    data = request.get_json()
    page = data["page"]

    # 数据库操作
    search = "select * from kunming_tushifang order by date desc limit "+str((page-1)*10)+",10"
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
        "total_price_guess":i[32],
        "plan_price_guess":i[33],
        "deviation_guess":i[34],
        "total_guess_rate":i[35],
        "total_rate":i[36],
        "file_path":i[39],
        "area":i[38],
        "ps":i[37]
        }

        list.append(dict)

    return json.dumps(list)

#最近一个查询
@app.route("/kunming/last")
def kunming_last():
    # 数据库操作
    search = "select * from kunming_tushifang order by date desc limit 1"
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
        "total_price_guess":i[32],
        "plan_price_guess":i[33],
        "deviation_guess":i[34],
        "total_guess_rate":i[35],
        "total_rate":i[36],
        "file_path":i[39],
        "area":i[38],
        "ps":i[37]
        }

        list.append(dict)

    return json.dumps(list)

# 页数
@app.route("/kunming/page")
def kunming_page():

    # 数据库操作
    search = "select * from kunming_tushifang"
    cursor.execute(search)
    info = cursor.fetchall()


    return json.dumps(len(info))

# 昆明土石方图表页

# 累计出土方量计划值与实际值对比
@app.route("/kunming/real_vs_plan/total")
def kunming_r_vs_p_total():
    # 数据库操作
    search = "select date,day_out_total,plan_day_out from kunming_tushifang order by date"
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
@app.route("/kunming/real_vs_plan/day")
def kunming_r_vs_p_day():
    # 数据库操作
    search = "select date,day_out,plan_out,advice_out from kunming_tushifang order by date"
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
@app.route("/kunming/circle/real_vs_plan")
def kunming_circle_r_vs_p():
    # 数据库操作
    search = "select date,day_out_total,plan_day_out from kunming_tushifang order by date desc limit 1"
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
@app.route("/kunming/circle/rate_vs_daysrate")
def kunming_circle_rate_vs_daysrate():
    # 数据库操作
    search = "select day_out_total,days,days_gone from kunming_tushifang order by date desc limit 1"
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
@app.route("/kunming/pie/out_vs_remain")
def kunming_pie_out_vs_remain():
    # 数据库操作
    search = "select day_out_total,out_remain from kunming_tushifang order by date desc limit 1"
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
@app.route("/kunming/pie/days_vs_gone")
def kunming_pie_days_vs_gone():
    # 数据库操作
    search = "select days,days_gone from kunming_tushifang order by date desc limit 1"
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
@app.route("/kunming/week/out")
def kunming_week_out():
    # 数据库操作
    search = "select date,day_out from kunming_tushifang order by date desc limit 14"
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
@app.route("/kunming/week/out_total")
def kunming_week_out_total():
    # 数据库操作
    search = "select date,day_out from kunming_tushifang order by date desc limit 14"
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
@app.route("/kunming/watch/days_gone")
def kunming_watch_days_gone():
    # 数据库操作
    search = "select days_gone,days from kunming_tushifang order by date desc limit 1"
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
@app.route("/kunming/watch/total")
def kunming_watch_total():
    # 数据库操作
    search = "select days_gone from kunming_tushifang order by date desc limit 1"
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
