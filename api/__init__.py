#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-15 00:31
# @File    : __init__.py
from api.api_host import ApiHost
from api.api_service import ServiceApi
from application_config import application

application.register_blueprint(ApiHost, url_prefix='/api/host')
application.register_blueprint(ServiceApi, url_prefix='/api/service')
