#coding:utf-8
import configparser
import os

conf = configparser.ConfigParser()


def readConf():
    '''读取配置文件'''
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conf.read(root_path + 'db.conf')  # 文件路径
    print(conf)
    name = conf.get('mysql',"host")  # 获取指定section 的option值
    print(name)


readConf()
