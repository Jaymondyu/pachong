# encoding:utf-8
import flask
import json
import datetime
import requests
import time
import random


#================================================================================================================
# OAuth 利用id和secret换取Token

# 利用dict对Token进行缓存
cache = {}

def _GetToken(scope):
	if cache.get(scope) and time.time()<cache[scope]['expire_at']:
		# print(u"GetToken(): 缓存命中")
		return cache[scope]['access_token']

	client_id = 'tNq6FSBKOQAk7XOCGqhP5z5Bu9sNj1Lo'
	client_secret = 'ydoGkbAxZwlHYqV2'

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
	access_token = respose['access_token']
	cache[scope] = {}
	cache[scope]['expire_at'] = time.time() + 3599
	cache[scope]['access_token'] = access_token
	return access_token

def GetPublicToken():
	return _GetToken("viewables:read")

def GetInternalToken():
	return _GetToken("data:read")

app = flask.Flask(__name__)

@app.route("/")
def index():
	return flask.render_template("index.html")


@app.route("/token")
def AccessToken():
	return json.dumps({"access_token": GetPublicToken()})


#---------------------------------------------------------------------------
# 时间接口：可以计算时间的差值
@app.route("/date/remain")
def remaining_days():
	d = flask.request.args.get("d", "2019-10-31").split("-")
	Y, M, D = int(d[0]), int(d[1]), int(d[2])
	d = datetime.datetime(Y, M, D) - datetime.datetime.now()
	return json.dumps([{"days": d.days}])


@app.route("/date/begin")
def begining_days():
	d = flask.request.args.get("d", "2017-01-01").split("-")
	Y, M, D = int(d[0]), int(d[1]), int(d[2])
	d = datetime.datetime.now() - datetime.datetime(Y, M, D)
	return json.dumps([{"days": d.days}])


#---------------------------------------------------------------------------
# 天气接口：从天气局获取数据
weather_cache = None
ALERTURL = "//datav.oss-cn-hangzhou.aliyuncs.com/uploads/images/59fae7694b5725e4b874bbfa55372489.png"
@app.route("/weather")
def get_weather():
	global weather_cache
	now = time.time()
	if weather_cache and now - weather_cache[0]<7200:
		d = weather_cache[1]
	else:
		r = requests.get("https://www.tianqiapi.com/api/?version=v1&city=深圳")
		d = json.loads(r.content)['data'][0]
		weather_cache = (now, d)

	text = d['wea'] + "  " + d['tem2'] + " ~ " + d['tem1']
	url = ALERTURL if u"雨" in text else ""
	return json.dumps([{"value":  text, "img": url}])


#---------------------------------------------------------------------------
# 环境数据：编造监测数据
@app.route("/env")
def get_env():
	t = flask.request.args.get("type", "text")
	pm25 = random.random() * 3 + 21.5
	pm10 = random.random() * 5 + 25.5
	noise = random.random() * 4 + 20
	if t == "text":
		return json.dumps([{"value":"pm2.5:%.1f pm10:%.1f 噪音:%.1fdb" % (pm25,pm10,noise)}])
	else:
		return json.dumps([{"pm2.5": pm25, "pm10":pm10, "noise":noise}])


#---------------------------------------------------------------------------
# 视频数据：获取RTMP流地址
rtmps = ["rtmp://rtmp01open.ys7.com/openlive/2115c71259ee45dc8314e092dead30d3","rtmp://rtmp01open.ys7.com/openlive/48876c3e93714fd399d41d03ab3d50f8","rtmp://rtmp01open.ys7.com/openlive/cd3e43b7a2574835a21e94886e800d09","rtmp://rtmp01open.ys7.com/openlive/e3677c17412a4ee199cf233eaf33264d","rtmp://rtmp01open.ys7.com/openlive/7c8230b81c524364b24985d2fce24617","rtmp://rtmp01open.ys7.com/openlive/a1d241a2a4784d80a3679d0074ef9379","rtmp://rtmp01open.ys7.com/openlive/c27098a99fab4180921ecf571a5f6d77","rtmp://rtmp01open.ys7.com/openlive/00d84a4d89b241d58d6c226c83b321da","rtmp://rtmp01open.ys7.com/openlive/1c1d4a1d83ba4276827cd90f763cb7a4","rtmp://rtmp.open.ys7.com/openlive/366370937b2442658e2492159bc2e38d"]
@app.route("/webcam")
def get_video():
	try:
		vid = flask.request.args.get("vid", 0)
		link = rtmps[int(vid)]
		res = [{"source": link}]
	except:
		res = [{"source": rtmps[0]}]
	return json.dumps(res)

application = app
if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8808, debug=True)
