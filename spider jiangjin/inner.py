#encoding:utf-8
import re
import sys
import time
import chardet
import requests
import sqlite3

def print_users():
	'''
	获取最新的用户列表
	'''
	db = sqlite3.connect("user.db")
	cur = db.cursor()
	cur.execute("SELECT * FROM USER")

	for i,u,n in [(u"index",u"user",u"name")] + cur.fetchall():
		print "%5s%20s  %s"%(i,u,n)

def get_cookies():
	'''
	获取管理员登陆信息的cookie
	'''
	url = "http://www.tylin-js.com.cn/index.php/admin/public/dologin"
	data = {
		"username": "admin",
		"password": "admin@lty.com.cn",
		"verify": 1
	}
	r = requests.post(url, data=data)

	cookies = dict(r.cookies)
	cookies.update({"3gIHlF_think_language": "zh-CN"})
	return cookies

# 指令 -U
def update_users():
	'''
	获取最新的用户列表
	'''
	cookies = get_cookies()
	db = sqlite3.connect("user.db")
	cur = db.cursor()
	# 清空数据库
	cur.execute("DELETE FROM USER")
	db.commit()
	# 起始URL
	url = "http://www.tylin-js.com.cn/index.php/user/admin_user/index/menuid/134/p/1"
	while True:
		print "retrieving %s"%url
		r = requests.get(url,cookies=cookies)
		html = r.content
		for ID, user, name in re.findall(r"<td align='center'>(\d+)</td> <td>(.+?)</td> <td>(.+?)</td>",html):
			ID = int(ID)
			user = user.decode("utf-8")
			name = name.decode("utf-8")
			try:
				cur.execute("INSERT INTO USER VALUES(?,?,?)", (ID, user, name))
			except sqlite3.IntegrityError:
				continue
		db.commit()
		time.sleep(0.3)
		try: # 获取下一页的URL
			url = "http://www.tylin-js.com.cn"+re.findall(r"<a href=\"(\S+?)\">下一页</a>", html)[0]
		except Exception as e:
			print "finished!"
			break

def add_single(user, cookies):
	url = "http://www.tylin-js.com.cn/index.php/user/admin_user/add_post"
	data = {
		"user_type": "2",
		"user_login": user,
		"user_pass": "123",
		"user_email": user+"@tylin.com.cn",
		"role_id[]": "0"
	}
	r = requests.post(url,cookies=cookies,data=data)
	if r.status_code == 200:
		if "成功" in r.content:
			print u"用户[%s]注册成功！"%user
		else:
			print u"用户[%s]注册失败："%user + re.findall(r"<li>(.+?)</li>",r.content.decode("utf-8"))[0]
	else:
		print u"用户[%s]注册失败：网络错误，返回码 %d"%(user,r.status_code)

# 指令：-A
def add(fn="input.txt"):
	cookies = get_cookies()
	time.sleep(0.3)
	lines = open(fn).readlines()
	for line in lines:
		line = line.strip()
		if len(line) == 0:
			continue
		enc = chardet.detect(line);
		if (enc['confidence'] > 0.9) and (enc['encoding'] == 'ascii'):
			print u"注册用户[%s]中..."%line
			add_single(line, cookies)
			time.sleep(0.3)

def remove_single(userID, cookies):
	url = "http://www.tylin-js.com.cn/index.php/user/admin_user/delete/id/%d"%userID
	r = requests.get(url,cookies=cookies)
	if r.status_code == 200:
		if "成功" in r.content:
			print u"用户[%d]删除成功！"%userID
		else:
			print u"用户[%d]删除失败："%userID
	else:
		print u"用户[%d]注册失败：网络错误，返回码 %d"%(user,r.status_code)

def get_userID(user, delete_user=True):
	db = sqlite3.connect("user.db")
	cur = db.cursor()
	cur.execute("SELECT ID FROM USER WHERE USER=?",(user,))
	res = cur.fetchone()
	if res:
		if delete_user:
			cur.execute("DELETE FROM USER WHERE USER=?",(user,))
			db.commit()
		return res[0]
	else:
		return None

# 指令：-R
def remove(fn="input.txt"):
	cookies = get_cookies()
	time.sleep(0.3)
	lines = open(fn).readlines()
	for line in lines:
		line = line.strip()
		if len(line) == 0:
			continue
		enc = chardet.detect(line);
		if (enc['confidence'] > 0.9) and (enc['encoding'] == 'ascii'):
			userID = get_userID(line)
			if userID is None:
				print u"不存在用户[%s]，请核对或刷新列表信息"%line
			else:
				print u"删除用户[%s]中..."%line
				remove_single(userID, cookies)
				time.sleep(0.3)

argv = sys.argv
HELP=u'''无法解析指令，使用方法如下：
-U 更新用户列表
-L 打印所有用户信息
-A [filename] 批量添加用户
-R [filename] 批量移除用户
filename若空缺则默认为input.txt'''
if len(argv)<2:
	print HELP
	exit(0)

instruction = argv[1]
if instruction == "-U":
	update_users()
elif instruction == "-L":
	print_users()
elif instruction == "-A":
	try:
		fn = argv[2]
	except:
		fn = "input.txt"
	add(fn)
elif instruction == "-R":
	try:
		fn = argv[2]
	except:
		fn = "input.txt"
	remove(fn)
else:
	print HELP