
# -*-encoding: utf-8 -*-
"""
@version: 3.6
@time: 2018/6/9 10:16
@author: SunnyYang
"""
import os,sys
import datetime
import smtplib
import traceback
import schedule
import time

from email.header import Header
from email.utils import parseaddr,formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders



# 对名字前面的中文进行处理
def _format_addr(s):
    name,addr = parseaddr(s)
    print(name)  #Python爱好者ii
    print(addr)   #Wangxyid@163.com
    return formataddr((Header(name,'utf-8').encode(),addr))

def send_email(to_str_in,alarm):
    #配置邮件的发送和接受人
    from_str = 'wangxiuli@tylin.com.cn'   #发送邮件人的邮箱地址
    password = 'Welcome@tylin'  #邮箱的客户端授权码，不是邮箱的登录密码
    smtp_server = 'smtp.tylin.com.cn' #163邮箱的服务器地址
    to_addr = to_str_in    #邮件的接收人

    #邮件发送人和接受人信息
    msg = MIMEText(alarm,"plain",'utf-8')
    msg['From'] = _format_addr('曹伟<%s>' % from_str)
    msg['To'] = _format_addr('<%s>' % to_addr)
    msg['Subject'] = Header('项目预警','utf-8').encode()

    time.sleep(0.6)
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)  # 用于显示邮件发送的执行步骤
    server.login(from_str, password)
    server.sendmail(from_str, to_addr, msg.as_string())
    server.quit()

while 1:
    current_time = datetime.datetime.now().strftime('%H:%M:%S')

    if current_time == "00:39:00":

        send_email('18875001129@163.com',"这是一个测试邮件")
        continue
