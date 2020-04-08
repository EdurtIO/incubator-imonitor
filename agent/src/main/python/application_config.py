#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:52:27
# @Desc    : app配置
# @File    : application_config.py
import sys
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

app.config['SECRET_KEY'] = 'haha'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


