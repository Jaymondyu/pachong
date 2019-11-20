# -*- coding: utf-8 -*-
# 获取forge token接口

import requests
import json
import logging
from cacheout import Cache
from flask import jsonify
from flask import Blueprint

routecert = Blueprint('routecert', __name__)
client_id = "AImdFVubhBVGfvxBaisnGZLbAnWDRAKo"
client_secret = "MJGgNr2vKsLiuK1C"
cache = Cache()


# get forge token
def GetToken(scope):
	if cache.get(scope):
		# print(u"GetToken(): 缓存命中")
		return cache.get(scope)

	url = "https://developer.api.autodesk.com/authentication/v1/authenticate"
	headers = {"Content-Type": "application/x-www-form-urlencoded"}
	body = {
		"client_id": client_id,
		"client_secret": client_secret,
		"grant_type": "client_credentials",
		"scope": scope
	}
	r = requests.post(url, headers=headers, data=body)
	response_txt = json.loads(r.text)
	logging.warning("autodesk api return ->")
	logging.warning(response_txt)
	access_token = response_txt['access_token']
	cache.set(scope, access_token, ttl=3599)
	return access_token


# get forge token
def GetTokenDefault():
	return GetToken("data:read")


'''
json format:
{
	"token": "T3lDV9vdSE1pUUImsEh7R-pi5fKHY"
}
'''
# get forge token
@routecert.route("/gettoken", methods=["GET"])
def GetTokenAPI():
	access_token = GetTokenDefault()
	rtn_data = {'token': access_token}
	return jsonify(rtn_data)



