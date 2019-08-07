from flask import Flask,request
import mysql.connector
import json

app = Flask(__name__)

conn = mysql.connector.connect(user = 'root',password ='plokijuh9',database ='j') #连接数据库，创建Flask_app数据库
cursor = conn.cursor()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/insert" ,methods=["POST"])
def insert():
    data = request.get_json()

    event_name = data['event_name']
    plan_time = data["plan_time"]
    finish_time = data["finish_time"]
    dpi = data["dpi"]

    sql = "INSERT INTO test_alarm (event_name, plan_time, finish_time, dpi) VALUES ("+ event_name + ","+ plan_time + "," + finish_time + "," + str(dpi) + ")"

    # cursor.execute(sql)




    return sql

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
