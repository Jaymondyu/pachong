# -*- coding: utf-8 -*-
import flask
import pymssql
from math import ceil
import json
import requests
import time
import uuid
import os
from kafka import KafkaConsumer
from flask import Blueprint

# app = flask.Flask(__name__)
# application = app
cache = {}
client_id = "AImdFVubhBVGfvxBaisnGZLbAnWDRAKo"
client_secret = "MJGgNr2vKsLiuK1C"

forgeupload = Blueprint('forgeupload', __name__)

def Upload(bucketName, filePath, fileName, tryNum):
    conn = pymssql.connect(host='172.168.10.130', user='bcmpadmin', password='WelcomeBcmp', database='ecology')
    c = conn.cursor()
    url = "https://developer.api.autodesk.com/oss/v2/buckets/%s/objects/%s/resumable" % (bucketName, fileName)
    size = os.path.getsize(filePath)
    chunkSize = 3 * 1024 * 1024
    num_chunks = int(ceil(1. * size / chunkSize))
    accessToken = GetToken("data:write data:create")
    GUID = str(uuid.uuid1())
    f = open(filePath, "rb")
    for i in range(num_chunks):
        start = i*chunkSize
        end = min((i+1)*chunkSize-1, size-1)
        real_size = end - start + 1

        headers = {
            "Authorization": "Bearer %s" % accessToken,
            "Content-Length": str(int(real_size)),
            "Content-Range": "bytes %d-%d/%d"%(start, end, size),
            "Session-Id": GUID
        }
        data = f.read(chunkSize)
        # print(num_chunks)
        r = requests.put(url, headers=headers, data=data)
        print(type(r.status_code))

        if r.status_code > 202:
            # print("error")
            if tryNum >= 3:
                sql = "UPDATE zbcmp_pub_model_upload SET upload_status = 2 WHERE file_path = '%s'"%(filePath)
                c.execute(sql)
                conn.commit()
                conn.close()
                return "too many attemps"
                #在数据库中标记为上传失败文件
            else:
                tryNum += 1
                Upload(bucketName, filePath, fileName, tryNum)

        if r.status_code == 202:
            # print("202")
            sql = "UPDATE zbcmp_pub_model_upload SET upload_process = %s WHERE file_path = '%s'" % ((i + 1) / float(num_chunks) * 100, filePath)
            # print(sql)
            c.execute(sql)
            conn.commit()
        else:
            sql = "UPDATE zbcmp_pub_model_upload SET upload_process = %s WHERE file_path = '%s'" % (100, filePath)
            c.execute(sql)
            sql = "UPDATE zbcmp_pub_model_upload SET upload_status = %s WHERE file_path = '%s'" % (1, filePath)
            c.execute(sql)
            conn.commit()
            conn.close()
            return r.status_code

#获取token
def GetToken(scope):
	if cache.get(scope) and time.time()<cache[scope]['expire_at']:
		# print(u"GetToken(): 缓存命中")
		return cache[scope]['accessToken']

	# print(u"GetToken(): 无Token信息或失效，通过网络获取")
	url = "https://developer.api.autodesk.com/authentication/v1/authenticate"
	headers = { "Content-Type": "application/x-www-form-urlencoded" }
	body = {
		"client_id": client_id,
		"client_secret": client_secret,
		"grant_type": "client_credentials",
		"scope": scope
	}
	r = requests.post(url, headers=headers, data=body)
	respose = json.loads(r.text)
	accessToken = respose['access_token']
	cache[scope] = {}
	cache[scope]['expire_at'] = time.time() + 3599
	cache[scope]['accessToken'] = accessToken
	# print accessToken
	return accessToken

#创建bucket
@forgeupload.route("/creatbucket", methods=["GET"])
def CreatBucket():
    bucketName = flask.request.args.get('bucketName')
    accessToken = GetToken("bucket:create")
    # return accessToken
    url = "https://developer.api.autodesk.com/oss/v2/buckets"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + accessToken
    }
    body = json.dumps({
        "bucketKey": bucketName,
        "policyKey": "persistent"
    })
    # return body
    res = requests.post(url, headers = headers, data = body)
    print(res)
    print(res.text)
    return str(res)

#查询bucket
@forgeupload.route("/getbucket", methods=["GET"])
def GetBucket():
    accessToken = GetToken("bucket:read")
    url = "	https://developer.api.autodesk.com/oss/v2/buckets"
    headers = {
        "Authorization": "Bearer " + accessToken
    }
    res = requests.get(url, headers = headers)
    # print res.text
    return res.text

#查看bucket内文件（获取urn）
@forgeupload.route("/getfileurn", methods=["GET"])
def GetObjects():
    bucketName = flask.request.args.get('bucketName')
    accessToken = GetToken("data:read")
    url = "https://developer.api.autodesk.com/oss/v2/buckets/"+ bucketName +"/objects"
    headers = {
        "Authorization": "Bearer " + accessToken
    }
    # print accessToken
    res = requests.get(url, headers = headers)
    # print res
    return res.text


#模型转换
@forgeupload.route("/trans", methods=["GET"])
def TransObjectToSvf():
    urn = flask.request.args.get('urn')
    accessToken = GetToken("data:read data:create")
    url = "https://developer.api.autodesk.com/modelderivative/v2/designdata/job"
    headers = {
        "Authorization": "Bearer " + accessToken,
        "Content-Type": "application/json"
    }
    body = json.dumps({
        "input": {
            "urn": urn
        },
        "output": {
            "formats": [
                {
                    "type": "svf",
                    "views": ["3d"]
                }
            ]
        }
    })
    res = requests.post(url, headers = headers, data = body)
    # print res
    return res.text

#删除模型
@forgeupload.route("/delete", methods=["GET"])
def DeleteFile():
    urn = flask.request.args.get('urn')
    accessToken = GetToken("data:read data:write")
    url = "https://developer.api.autodesk.com/modelderivative/v2/designdata/" + urn + "/manifest"
    headers = {
        "Authorization": "Bearer " + accessToken
    }
    res = requests.delete(url, headers = headers)
    return res.text



consumer = KafkaConsumer('tpbcmp', group_id='group2', bootstrap_servers=['172.168.10.130:9092'])
for msg in consumer:
    msgObj = json.loads(msg.value.decode('utf-8'))
    try:
        fid = msgObj["data"]["fid"]
        conn = pymssql.connect(host='172.168.10.130', user='bcmpadmin', password='WelcomeBcmp', database='ecology')
        c = conn.cursor()
        sql = "SELECT bucket_name, file_path FROM zbcmp_pub_model_upload WHERE fid = 'fid'"%(fid)
        c.execute(sql)
        res = c.fetchall()[0]
        bucketName = res[0]
        filePath = res[1]
        fileName = filePath.split('/')[-1]
        Upload(bucketName, filePath, fileName, 1)
    except:
        pass


# if __name__ == '__main__':
#     app.run(host="0.0.0.0", debug=True, port=5000)
