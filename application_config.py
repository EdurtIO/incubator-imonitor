#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-13 22:31
# @File    : application_config.py
import logging
import os

import yaml
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# reload(sys)
# sys.setdefaultencoding('utf-8')

# logger
FORMAT = '%(asctime)-15s - %(name)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('iMonitor')
logger.setLevel(logging.DEBUG)

logger.info('load default configuration file to application starting ...')
path = os.path.join(os.path.dirname(__file__), 'configuration', 'default.yml')
file = None
try:
    file = open(path, 'r')
    configuration = yaml.load(file)
except Exception as e:
    logger.error('load default configuration file to application error, reason %s', e)
    exit(0)
finally:
    if file is not None:
        file.close()
    logger.info('load default configuration file to application stop ...')

application = Flask(__name__)

# database
logger.info('configuration database start ...')
application.config['SECRET_KEY'] = configuration['server']['secret']
application.config['SQLALCHEMY_DATABASE_URI'] = configuration['database']['url']
application.config['SQLALCHEMY_ECHO'] = configuration['database']['print-sql']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = configuration['database']['track']
logger.info('configuration database end ...')

bootstrap = Bootstrap(application)
moment = Moment(application)
db = SQLAlchemy(application)

# security framework
from flask_login import LoginManager

logger.info('configuration security framework start ...')
login_manager = LoginManager()
login_manager.init_app(application)
logger.info('configuration security framework end ...')
