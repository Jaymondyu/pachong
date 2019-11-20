# -- coding: utf-8 --
import flask
from flask import request
import json
import requests
import operator
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


DEBUG = False
if not DEBUG:
    import sys
    sys.path.append("/var/www/html/paltdata")
import db
cache = {}

app = flask.Flask(__name__)

application = app

locationList = [
            "昆明市综合交通国际枢纽建设项目",
            "昆明市官渡区人民医院迁建项目",
            "深圳书城龙华城建设项目",
            "重庆市江津区滨江商务大厦工程",
            "重庆市綦江城区环城大道建设转关口大桥段工程",
            "悦来会展总部基地项目",
            "重庆市残疾人康复中心（一期）工程"
        ]

orgDic = {
  "中京华（北京）工程咨询有限公司": "跟审单位",
  "林同棪（重庆）国际工程技术有限公司": "监理单位",
  "重庆悦瑞文化旅游发展有限公司": "建设单位",
  "重庆博建建筑规划设计有限公司": "设计单位",
  "中国建筑第八工程局有限公司": "施工单位",
  "重庆市綦江区城市建设投资有限公司": "建设单位",
  "中铁建大桥局集团有限公司": "施工单位",
  "重庆求精工程造价有限责任公司": "造价单位",
  "昆明市官渡区人民医院迁建项目": "政府部门"
}


locationDic = {
    "昆明市官渡区人民医院迁建项目":"官渡医院",
    "深圳书城龙华城建设项目": "龙华书城",
    "重庆市江津区滨江商务大厦工程": "江津滨江",
    "重庆市綦江城区环城大道建设转关口大桥段工程": "綦江大桥",
    "悦来会展总部基地项目": "悦来基地",
    "重庆市残疾人康复中心（一期）工程": "残联中心",
    "昆明市综合交通国际枢纽建设项目": "昆明枢纽",

}

@app.route("/getprojects")
def Getprojects():
    return json.dumps(db.Getprojects())


@app.route("/getregorgbylocationanddate", methods=["POST"])
def Getregorgbylocationanddate():
    data = flask.request.get_json()
    location = data["location"]
    time1 = data["time1"]
    time2 = data["time2"]
    limit1 = int(data["limit1"])
    dateLis = []
    orgDivLis = []
    orgLis = map(OrgMap, db.Getregorgbylocationanddate(location, time1, time2))
    for i in orgLis:
        if (i["date"] in dateLis):
            pass
        else:
            dateLis.append(i["date"])
            orgDivLis.append([])
            for j in orgLis:
                if j["date"] == i["date"]:
                    orgDivLis[-1].append(j)

    l = len(orgDivLis)
    lis = map(GetOrgName, orgDivLis[-1])
    for org in lis:
        for i in range(len(orgDivLis) - 1):
            if org in map(GetOrgName, orgDivLis[i]):
                pass
            else:
                orgDivLis[i].append({"orgName": org, "regNum": 0, "date": orgDivLis[0]["date"]})

    for i in range(len(orgDivLis)):
        for j in range(len(orgDivLis[i])):
            _name = orgDivLis[i][j]["orgName"].encode('utf8')
            # print _name
            # print orgDic.has_key(_name)
            if orgDic.has_key(_name):
                # print "1"
                orgDivLis[i][j]["orgName"] = orgDic[_name]
                # print orgDic[_name]
    return json.dumps({"data": map(SortDicts, orgDivLis)[limit1*5:limit1*5+5], "total": l})

def GetOrgName(lis):
    return lis["orgName"]

def SortDicts(dicLis):
    return sorted(dicLis, key = operator.itemgetter('orgName'))



@app.route("/getregnumbylocationanddate", methods=["POST"])
def Getregnumbylocationanddate():
    data = flask.request.get_json()
    location = data["location"]
    time1 = data["time1"]
    time2 = data["time2"]
    limit1 = data["limit1"]
    limit2 = data["limit2"]
    return json.dumps(map(NumMap, db.Getregnumbylocationanddate(location, time1, time2, limit1, limit2)))

@app.route("/getlocationschart", methods=["POST"])
def Getlocationschart():
    data = flask.request.get_json()
    time = data["time2"]
    locationRegLis = []
    for location in locationList:
        # print location
        # print time
        # print db.Getregnumbylocationanddate(location, time, time, 0, 1)[0][0]
        locationRegLis.append(db.Getregnumbylocationanddate(location, time, time, 0, 1)[0][0])
    _locationList = locationList[:]
    for i in range(len(_locationList)):
        if locationDic.has_key(_locationList[i]):
            _locationList[i] = locationDic[_locationList[i]]
    # print {"x": _locationList, "y": locationRegLis}["x"][0]
    return json.dumps({"x": _locationList, "y": locationRegLis})

@app.route("/getaccess", methods=["POST"])
def Getaccess():
    data = flask.request.get_json()
    location = data["location"]
    time1 = data["time1"]
    time2 = data["time2"]
    url = "http://www.tylinbim.com/4DAnalog/lintyData/queryHrmlog.action?logType=TN&regName=%s&startDate=%s&endDate=%s" %(location, time1, time2)
    res = requests.get(url)
    restext = res.text
    bodyObj = json.loads(restext)["data"]
    dayLis = []
    returnLis = []
    coarseOrgLis = []
    for body in bodyObj:
        otherOrgNum = 0
        bimOrgNum = 0
        for org in body["detail_list"]:
            dayLis.append({"org_name": org["org_name"], "access_num": org["access_num"], "access_date": org["access_date"]})
            if org["org_name"] == u"BIM咨询单位":
                bimOrgNum += org["access_num"]
            else:
                otherOrgNum += org["access_num"]
        returnLis.append(dayLis)
        coarseOrgLis.append({"bim": bimOrgNum, "other": otherOrgNum, "access_date": org["access_date"]})
    return json.dumps({"detail": returnLis, "course": coarseOrgLis})



def OrgMap(tup):
    return { "orgName": tup[0], "regNum": tup[1], "date": str(tup[2])}

def NumMap(tup):
    return { "allNum": tup[0], "addNum": tup[1], "deleNum": tup[2], "date": str(tup[3])}



# aaaa = "林同棪（重庆）国际工程技术有限公司"
# print orgDic.has_key(aaaa)




























if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
