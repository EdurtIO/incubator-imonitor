#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:52:27
# @Desc    : app配置
# @File    : application_config.py
import os
import sys

import yaml
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# reload(sys)
# sys.setdefaultencoding('utf-8')

config_name = 'config.yaml'

path = os.path.join(os.path.dirname(__file__), 'config', config_name)
file = None
try:
    file = open(path, 'r')
    codes = yaml.load(file, Loader=yaml.FullLoader)
finally:
    if file is not None:
        file.close()

app = Flask(__name__)

app.config['SECRET_KEY'] = codes['server']['secret']
app.config['SQLALCHEMY_DATABASE_URI'] = codes['server']['db']['uri']
app.config['SQLALCHEMY_ECHO'] = codes['server']['db']['print-sql']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = codes['server']['db']['track']

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

## 启用权限框架
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

