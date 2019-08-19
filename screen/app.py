#coding:utf-8
from flask import Flask,request,render_template
import mysql.connector
import json
import time
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    