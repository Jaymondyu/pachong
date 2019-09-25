#coding:utf-8
import mysql.connector
import datetime
import os
import json





conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123',database ='shenzhen_event',auth_plugin='mysql_native_password') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()

data = {
    "date" :"2019-7-11",
    "car_amount" :12,
    "zhachang" :"???",
    "distance" :"",
    "digger_amount" :11,
    "day_car_out" :15,
    "day_out" :500,
    "manager" : " 王俊凯",
    "area" :"333",
    "ps" :"222",
    "file_path" :"111"
}

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
    search = "select day_out from yuelai__tushifang__test where date <" + "'" + str(date) + "'"
    cursor.execute(search)
    result = cursor.fetchall()
    sum = 0
    for i in result:
        sum = sum + i[0]
    return sum

# 实际累计出土车数
def leiji_che(date):
    search = "select day_car_out from yuelai__tushifang__test where date <" + "'" + str(date) + "'"
    cursor.execute(search)
    result = cursor.fetchall()
    sum = 0
    for i in result:
        sum = sum + i[0]
    return sum
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
rate = day_out_total/out_total                   # 实际完成比例(=实际累计出土方量/总土石方量)
plan_rate = plan_day_out/out_total               # 计划完成比例(=计划累计出土方量/总土石方量)
deviation_rate = rate - plan_rate                # 比例偏差(=实际完成比例-计划完成比例)

# 调整建议
advice_out = out_remain/days_remain               # 后续每日建议出土方量(=实际剩余土石方量/剩余工期)
advice_car = advice_out/car_take                # 后续每日建议出土车数(=实际剩余土石方量/剩余工期/核载量)




print days_gone
print days_remain
print day_out_total
print plan_day_out
print deviation_out
print out_remain
print plan_out_remain
print deviation_remain
print car_amount_total
print car_amount_plan
print deviation_car_amount
print rate
print plan_rate
print deviation_rate
print advice_out
print advice_car
