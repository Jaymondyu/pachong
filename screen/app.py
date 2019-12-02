from flask import Flask,render_template
import flask
# DEBUG = False
# if not DEBUG:
import sys
sys.path.append("/var/www/html/screen/")
from jiangjin import jiangjin
from yuelai import yuelai
from canlian import canlian

app = Flask(__name__)

app.register_blueprint(jiangjin, url_prefix='/jiangjin')
app.register_blueprint(yuelai, url_prefix='/yuelai')
app.register_blueprint(canlian, url_prefix='/canlian')

@app.route('/test')
def hello_world():
    return 'Hello World!'

@app.route("/jiangjin")
def jiangjin_index():
    return render_template("jiangjin_index.html")

@app.route("/yuelai")
def yuelai_index():
    return render_template("index_yuelai.html")

@app.route("/canlian")
def canlian_index():
    return render_template("index_canlian.html")





application = app
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8082)