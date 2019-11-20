# -*- coding: utf-8 -*-

from flask import Flask
from service.V1.fg.certification import routecert
from service.V1.fg.uploadmodellocal import uploadmodellocal
# from service.V1.fg.uploadforge import forgeupload

app = Flask(__name__)

app.register_blueprint(routecert, url_prefix='/v1/fg/certification')

app.register_blueprint(uploadmodellocal, url_prefix='/v1/fg/uploadmodellocal')
#
# app.register_blueprint(uploadforge, url_prefix='/v1/fg/uploadforge')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8082)
