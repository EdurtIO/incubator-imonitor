#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-04-27 21:57
# @File    : view_server.py
from flask import Blueprint

server_view = Blueprint('server_view', __name__, template_folder='templates')

logger_type = 'server_view'
