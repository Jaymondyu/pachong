#coding:utf-8
from flask import Flask,request
import mysql.connector
import json
import time
import datetime
import config




# app = Flask(__name__)
#
# conn = mysql.connector.connect(config)
# cursor = conn.cursor()