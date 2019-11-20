# -*- coding: utf-8 -*-
import pymssql
import flask
import json
import requests
import time
import os
import datetime
import random
from kafka import KafkaProducer
from flask import Blueprint

uploadmodellocal = Blueprint('uploadmodellocal', __name__)

app = flask.Flask(__name__)
application = app

conn = pymssql.connect(host='172.168.10.130',user= 'bcmpadmin',password ='WelcomeBcmp', database = 'ecology')
cursor = conn.cursor()


# 接受前端文件并放至服务器
@uploadmodellocal.route("/upload",methods=["POST"])
def photo():

    file = flask.request.files.get("file")
    projectId = flask.request.args.get("projectId")
    fileName = flask.request.args.get("fileName")
    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = "%06d" % random.randint(0, 999999)
    name = fileName
    name = name.split(".")
    name_1 = str(projectId)+ str(now_time)+str(random_str)
    name = name_1+'.'+name[1]
    path = "d:/bimfile/%s/"%projectId
    if os.path.exists(path) == True:
        file_path = path + name
        file.save(file_path)
        location = file_path
        sql = "insert into zbcmp_pub_model_upload (file_path,file_name,project_id) values(%s,%s,%d)"%("'"+str(location)+"'","'"+fileName+"'",int(projectId))
        cursor.execute(sql)
        conn.commit()
    else:
        os.makedirs(path)
        file_path = path + name
        file.save(file_path)
        location = file_path
        sql = "insert into zbcmp_pub_model_upload (file_path,file_name,project_id) values(%s,%s,%d)" % ("'" + str(location) + "'", "'" + fileName + "'",int(projectId))
        cursor.execute(sql)
        conn.commit()

    sql = "select fid from zbcmp_pub_model_upload where file_path=%s"%("'" + str(location) + "'")

    producer = KafkaProducer(bootstrap_servers=['172.168.10.130:9092'])
    cursor.execute(sql)
    res = cursor.fetchall()[0][0]
    body = {
        "code": "FG001",
        "data": {"fid": res}
    }
    future = producer.send('tpbcmp', key=b'my_key', value=json.dumps(body).encode('utf-8'), partition=0)
    result = future.get(timeout=10)
    print(result)
    return json.dumps({"StatusCode":"200"})



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)