# -- coding: utf-8 --
import flask
from flask import request
import json
import requests
import datetime
import db
import time

locationList = [
            "昆明市综合交通国际枢纽建设项目",
            "昆明市官渡区人民医院迁建项目",
            "深圳书城龙华城建设项目",
            "重庆市江津区滨江商务大厦工程",
            "重庆市綦江区环城大道建设转关口段工程",
            "悦来会展总部基地项目",
            "重庆市残疾人康复中心（一期）工程"
        ]

def GetRegData():
    stTime = datetime.date.today()
    endTime = stTime

    for location in locationList:
        url = "http://www.tylinbim.com/4DAnalog/lintyData/queryOrgDtl.action?regName=%s&startDate=%s&endDate=%s"%(location, stTime, endTime)
        res = requests.get(url)
        data = json.loads(res.text)
        detailList = data["data"]["detail_list"]
        for i in detailList:
            na = i["org_name"]
            if i["org_id"] == 634:
                na = u"项目管理单位"
            elif i["org_id"] == 635:
                na = u"BIM咨询单位"
            db.Add2DetailTable(location, str(stTime), na, i["reg_num"])

        allNum_yesterday = data["data"]["reg_all_num"]
        addNum_yesterday = 0
        for i in data["data"]["hrm_add_list"]:
            addNum_yesterday += i["reg_add_num"]
        addNum_yesterday = len(data["data"]["hrm_add_list"])
        try:
            allNum_beforeyesterday = db.SeleAllNumFromChangeTable(location, stTime - datetime.timedelta(days=1))
            deleNum_yesterday = addNum_yesterday - (allNum_yesterday - allNum_beforeyesterday)
        except:
            deleNum_yesterday = 0

        db.Add2ChangeTable(location, stTime, allNum_yesterday, addNum_yesterday, deleNum_yesterday)
    return "200"
GetRegData()
