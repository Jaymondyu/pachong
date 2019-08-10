# encoding=utf-8
import smtplib
from email.header import Header
from email.utils import parseaddr,formataddr
from email.mime.text import MIMEText
import requests
import json


def get_address_late():

    data = requests.get("http://172.168.10.22:5000/table/email_late")
    data = data.text
    data = json.loads(data)
    b_dict = {}
    email_dict={}

    for event_email in data:
        b_dict[event_email[0]]=event_email[1]

    for k,v in b_dict.items():
        email_dict.setdefault(v, []).append(k)



    return email_dict



def get_address_near():

    data = requests.get("http://172.168.10.22:5000/table/email_near")
    data = data.text
    data = json.loads(data)





    b_dict = {}
    email_dict={}



    for event_email in data:
        b_dict[event_email[0]]=event_email[1]

    for k,v in b_dict.items():
        email_dict.setdefault(v, []).append(k)


    return email_dict



def _format_addr(s):
    name,addr = parseaddr(s)

    return formataddr((Header(name,'utf-8').encode(),addr))


def send_email_late(to_str_in,alarm):
    #配置邮件的发送和接受人
    from_str = 'wangxiuli@tylin.com.cn'   #发送邮件人的邮箱地址
    password = 'Welcome@tylin'  #邮箱的客户端授权码，不是邮箱的登录密码
    smtp_server = 'smtp.tylin.com.cn' #163邮箱的服务器地址
    to_addr = to_str_in    #邮件的接收人

    #邮件发送人和接受人信息
    msg = MIMEText(alarm,"plain",'utf-8')
    msg['From'] = _format_addr('曹伟<%s>' % from_str)
    msg['To'] = _format_addr('<%s>' % to_addr)
    msg['Subject'] = Header('项目滞后预警','utf-8').encode()


    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)  # 用于显示邮件发送的执行步骤
    server.login(from_str, password)
    server.sendmail(from_str, to_addr, msg.as_string())
    server.quit()

def send_email_near(to_str_in,alarm):
    #配置邮件的发送和接受人
    from_str = 'wangxiuli@tylin.com.cn'   #发送邮件人的邮箱地址
    password = 'Welcome@tylin'  #邮箱的客户端授权码，不是邮箱的登录密码
    smtp_server = 'smtp.tylin.com.cn' #163邮箱的服务器地址
    to_addr = to_str_in    #邮件的接收人

    #邮件发送人和接受人信息
    msg = MIMEText(alarm,"plain",'utf-8')
    msg['From'] = _format_addr('曹伟<%s>' % from_str)
    msg['To'] = _format_addr('<%s>' % to_addr)
    msg['Subject'] = Header('项目临近预警','utf-8').encode()


    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)  # 用于显示邮件发送的执行步骤
    server.login(from_str, password)
    server.sendmail(from_str, to_addr, msg.as_string())
    server.quit()


for i in get_address_late():

    event_list = get_address_late()[i]
    alarm = "事件" + str(event_list) +"已经处于滞后状态，请加快进度"
    to_str_in = i
    send_email_late(i,alarm)

for j in get_address_near():

    event_list = get_address_near()[i]
    alarm = "事件" + str(event_list) +"已经处于临近状态，请加快进度"
    to_str_in = i
    send_email_near(i,alarm)
