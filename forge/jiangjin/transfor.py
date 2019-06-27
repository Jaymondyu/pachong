# -*- coding: UTF-8 -*-
import os, requests, json
import time
import hashlib
import sqlite3
from urllib import quote

client_id = "OK54AyvODOgdSUmA9ivy04PwmzIZAP3g"
client_secret = "bvbwXbwI7HxO0lQ2"

cache = {}

urn = "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6cGxva2lqdWgxMjM0NTY3OC9CSUcubndk"
# urn3 = "urn:adsk.objects:os.object:drtnhxdwgh/project1.rvt"
# dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6ZHJ0bmh4ZHdnaC9wcm9qZWN0MS5ydnQ
# bucketKey = "drtnhxdwgh"
bucketKey = "plokijuh12345678"


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
	return accessToken

def GetPublicToken():
	return GetToken("viewables:read")

def GetInternalToken():
	return GetToken("data:read data:write data:create")

# print GetPublicToken()

def CreatBucket(bucketKey, accessToken):
    url = "https://developer.api.autodesk.com/oss/v2/buckets"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + accessToken
    }
    body = json.dumps({
        "bucketKey": bucketKey,
        "policyKey": "persistent"
    })
    res = requests.post(url, headers = headers, data = body)
    # print res.text
    return res

# print CreatBucket(bucketKey, GetToken("bucket:create"))

def GetBucket(accessToken):
    url = "	https://developer.api.autodesk.com/oss/v2/buckets"
    headers = {
        "Authorization": "Bearer " + accessToken
    }
    res = requests.get(url, headers = headers)
    # print res
    return res.text


def UploadFile(objectName, accessToken, bucketKey):
    size = os.path.getsize(objectName)
    url = "https://developer.api.autodesk.com/oss/v2/buckets/"+ bucketKey +"/objects/" + objectName
    headers = {
        "Content-Length": str(int(size)),
        "Authorization": "Bearer " + accessToken
    }
    body = open(objectName, "rb").read()
    return requests.put(url, headers = headers, data = body)

# print UploadFile("project1.rvt", GetToken("data:create"), bucketKey)

def GetObjects(bucketKey, accessToken):
    url = "https://developer.api.autodesk.com/oss/v2/buckets/"+ bucketKey +"/objects"
    headers = {
        "Authorization": "Bearer " + accessToken
    }
    # print accessToken
    res = requests.get(url, headers = headers)
    # print res
    return res.text

# print GetObjects(bucketKey, GetInternalToken())

def TransObjectToSvf(accessToken, urn):
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
# 先运行
# print TransObjectToSvf(GetInternalToken(), urn)

objTrees = {}

# 获取模型树信息
def GetObjectTree(urn, guid):
    if objTrees.has_key(guid):
    	# print(u"GetObjectTree(): 缓存命中")
    	return objTrees[guid]

    # print(u"GetObjectTree(): 无视图对象树信息，网络获取")
    token = GetInternalToken()
    url = "https://developer.api.autodesk.com/modelderivative/v2/designdata/%s/metadata/%s" % (urn, guid)
    headers = { "Authorization": "Bearer %s" % token }
    r = requests.get(url, headers = headers)
    objTree = json.loads(r.text)

    # 后处理！不然jstree无法处理！
    # 1. 取出树
    objTree = objTree['data']['objects']
    treetext = json.dumps(objTree)
    # 2. 更换key
    treetext = treetext.replace('"objects"', '"children"')
    treetext = treetext.replace('"name"', '"text"')
    treetext = treetext.replace('"objectid"', '"id"')
    objTrees[guid] = treetext
    return treetext

def GetObjectProperties(urn, guid):
	token = GetInternalToken()
	url = "https://developer.api.autodesk.com/modelderivative/v2/designdata/%s/metadata/%s/properties" % (urn, guid)
	headers = { "Authorization": "Bearer %s" % token }
	r = requests.get(url, headers=headers)
	res = json.loads(r.text)
	return res['data']['collection']

def GetObjectProperty(urn, guid, objectid):
	token = GetInternalToken()
	url = "https://developer.api.autodesk.com/modelderivative/v2/designdata/%s/metadata/%s/properties?objectid=%s" % (urn, guid, objectid)
	headers = { "Authorization": "Bearer %s" % token }
	r = requests.get(url, headers=headers)
	res = json.loads(r.text)
	return res['data']['collection'][0]['properties']

def GetGuid(urn):
    token = GetInternalToken()
    url = "https://developer.api.autodesk.com/modelderivative/v2/designdata/%s/metadata" % urn
    headers = { "Authorization": "Bearer %s" % token }
    res = requests.get(url, headers = headers)
    res = json.loads(res.text)
    return res["data"]["metadata"][0]["guid"].encode("utf-8")

def GetAllViewableThumbnails(urn):
	data = GetDocumentMenifest(urn)
	fns = dict()
	for child in data['derivatives'][0]['children']:
		if child['type'] == 'geometry':
			name = child['name']
			for child in child['children']:
				if child.get("resolution", [0])[0] == 400:
					derivativeurn = child['urn']
					thumbnail_path = GetViewableThumbnail(urn, derivativeurn)
					fns.update({name: "static/img/"+thumbnail_path})
	return fns

def GetDocumentMenifest(urn):
	token = GetInternalToken()
	url = "https://developer.api.autodesk.com/modelderivative/v2/designdata/%s/manifest" % urn
	headers = { "Authorization": "Bearer %s" % token }
	r = requests.get(url, headers=headers)
	r.raise_for_status()
	res = json.loads(r.text)
	return res
#再运行
print GetDocumentMenifest(urn)
exit(0)


def GetMarkup():
	db = sqlite3.connect("demo.sqlite")
	cur = db.cursor()
	cur.execute("SELECT id, name FROM MARKUP")
	data = [dict(zip(("id","name"), item)) for item in cur.fetchall()]
	return data

def GetMarkupByID(ID):
	db = sqlite3.connect("demo.sqlite")
	cur = db.cursor()
	cur.execute("SELECT state, data FROM MARKUP where ID = ?", (ID,))
	data = dict(zip(("state", "data"), cur.fetchone()))
	data['state'] = eval(data['state'])
	return data

# 添加标注
def AddMarkup(name, state, data):
	db = sqlite3.connect("demo.sqlite")
	cur = db.cursor()
	try:
		cur.execute("INSERT INTO MARKUP(name, state, data) VALUES (?,?,?)", (name, repr(state), data))
		db.commit()
	except sqlite3.IntegrityError:
		# 防止数据库被锁定
		db.close()
		raise Exception("标注名称需要唯一")
