# encoding=utf-8
import smtplib
from email.header import Header
from email.utils import parseaddr,formataddr
from email.mime.text import MIMEText
import requests
import json


def get_address_late():

   data = requests.get("http://183.66.213.82:8888/event/table/email_late")
   data = data.text

   data = json.loads(data)
   b_dict = {}
   email_dict={}

   for event_email in data:
       b_dict[event_email[0]]=event_email[1],event_email[2]

   for k,v in b_dict.items():
       email_dict.setdefault(v, []).append(k)


   return email_dict


def get_address_near():

   data = requests.get("http://183.66.213.82:8888/event/table/email_near")
   data = data.text
   data = json.loads(data)

   b_dict = {}
   email_dict={}

   for event_email in data:
       b_dict[event_email[0]]=event_email[1],event_email[2]

   for k,v in b_dict.items():
       email_dict.setdefault(v, []).append(k)


   return email_dict

def _format_addr(s):
    name,addr = parseaddr(s)

    return formataddr((Header(name,'utf-8').encode(),addr))

def send_email_late(to_str_in,alarm):
    #配置邮件的发送和接受人
    from_str = 'caowei@tylin.com.cn'   #发送邮件人的邮箱地址
    password = '743991oiw'  #邮箱的客户端授权码，不是邮箱的登录密码
    smtp_server = 'smtp.tylin.com.cn' #163邮箱的服务器地址
    to_addr = to_str_in    #邮件的接收人

    #邮件发送人和接受人信息
    msg = MIMEText(alarm,"plain",'utf-8')
    msg['From'] = _format_addr('曹伟<%s>' % from_str)
    msg['To'] = Header(",".join(to_addr))
    msg['Subject'] = Header('项目滞后预警','utf-8').encode()


    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)  # 用于显示邮件发送的执行步骤
    server.login(from_str, password)
    server.sendmail(from_str, to_addr, msg.as_string())
    server.quit()

def send_email_near(to_str_in,alarm):
    #配置邮件的发送和接受人
    from_str = 'caowei@tylin.com.cn'   #发送邮件人的邮箱地址
    password = '743991oiw'  #邮箱的客户端授权码，不是邮箱的登录密码
    smtp_server = 'smtp.tylin.com.cn' #163邮箱的服务器地址
    to_addr = to_str_in  # 邮件的接收人

    # 邮件发送人和接受人信息
    msg = MIMEText(alarm, "plain", 'utf-8')
    msg['From'] = _format_addr('曹伟<%s>' % from_str)
    msg['To'] = Header(",".join(to_addr))
    msg['Subject'] = Header('项目临近预警', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)  # 用于显示邮件发送的执行步骤
    server.login(from_str, password)
    server.sendmail(from_str, to_addr, msg.as_string())
    server.quit()


for i in get_address_late():
    data = requests.get("http://183.66.213.82:8888/shenzhen/date/remain?d=2019-11-02")
    data = data.text
    data = json.loads(data)
    data = data[0]["days"]

    count = requests.get("http://183.66.213.82:8888/event/table/count")
    count = count.text
    count = json.loads(count)
    count_all = count[0]["late"] + count[0]["near"] + count[0]["in_plan"] + count[0]["complete"]
    count_complete = count[0]["complete"]
    count_late = count[0]["late"]

    event_list = str(get_address_late()[i])
    alarm = (''' 尊敬的%s单位，您好!

    深圳书城龙华城项目截至今日，距离开业还有%d天，已经滞后项目汇总如下：

    %s

    请您及时处理协调存在问题，督促加快工作进程，保证工程顺利推进。

    (总销项任务数：%d件  已完成任务数：%d件 滞后任务数：%d件)''') % (
    i[1], data, event_list, count_all, count_complete, count_late)
    to_str_in = [i[0], "510096471@qq.com", "5045308@qq.com", "3387521919@qq.com", "hattieterry@foxmail.com"]
    send_email_late(to_str_in, alarm)




for j in get_address_near():
    data = requests.get("http://183.66.213.82:8888/shenzhen/date/remain?d=2019-11-02")
    data = data.text
    data = json.loads(data)
    data = data[0]["days"]

    count = requests.get("http://183.66.213.82:8888/event/table/count")
    count = count.text
    count = json.loads(count)
    count_all = count[0]["late"] + count[0]["near"] + count[0]["in_plan"] + count[0]["complete"]
    count_complete = count[0]["complete"]
    count_late = count[0]["near"]

    event_list = str(get_address_near()[j])
    alarm = (''' 尊敬的%s单位，您好!

    深圳书城龙华城项目截至今日，距离开业还有%d天，临近项目汇总如下：

    %s

    以上事件与您相关，请按时完成，保证工程顺利推进。

    (总销项任务数：%d件  已完成任务数：%d件 临近任务数：%d件)''') % (
    j[1], data, event_list, count_all, count_complete, count_late)
    to_str_in = [j[0], "510096471@qq.com", "5045308@qq.com", "3387521919@qq.com", "hattieterry@foxmail.com"]
    send_email_near(to_str_in, alarm)
