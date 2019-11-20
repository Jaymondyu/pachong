# -*- coding: utf-8 -*-
import pymssql
import flask
import json
import requests
import time
import os
import datetime


app = flask.Flask(__name__)
application = app

conn = pymssql.connect(host='172.168.10.130',user= 'bcmpadmin',password ='WelcomeBcmp', database = 'ecology')
cursor = conn.cursor()
# sql = "select * from zbcmp_pub_model_upload "
# # cursor.execute(sql)
# # res = cursor.fetchall()
# #
# # print(res)






# 接受前端文件并放至服务器
@app.route("/bcmp/services/v1/fg/object/upload/<projectId>/<fileName>",methods=["POST"])
def photo(projectId,fileName):

    file = flask.request.files.get("file")
    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    name = file.filename
    name = name.split(".")
    name_1 = str(projectId)+ str(now_time)
    name = name_1+'.'+name[1]
    path = "d:/bimfile/%s"%projectId
    file_path = path + name
    file.save(file_path)
    location = file_path
    sql = "insert into zbcmp_pub_model_upload (file_path,file_name) values(%s,%s)"%("'"+str(location)+"'","'"+fileName+"'")
    cursor.execute(sql)
    conn.commit()
    return json.dumps({"StatusCode":"200"})



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
