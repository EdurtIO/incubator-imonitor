#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-15 14:12:40
# @Desc    : 数据报表脚本
# @File    : api_chart.py
import json

from flask import Blueprint
from flask_login import login_required
from flask_restful import request

from model.service import ServiceModel
from services.service import Service
from utils.utils_parameter import Parameter
from utils.utils_response import Response

ServiceApi = Blueprint('ServiceApi', __name__, template_folder='templates')


@ServiceApi.route('', methods=['POST'])
# @login_required
def create():
    if request.data is not None:
        values = json.loads(request.data)
        service = ServiceModel()
        service.name = Parameter.getValue(source=values, key='name')
        service.compile_way = Parameter.getValue(source=values, key='binary')
        if service.compile_way is 0:
            service.compile_git = Parameter.getValue(source=values, key='compile_git')
            service.compile_git_username = Parameter.getValue(source=values, key='compile_git_username')
            service.compile_git_password = Parameter.getValue(source=values, key='compile_git_password')
        if service.compile_way is 1:
            service.binary = Parameter.getValue(source=values, key='binary')
        service.install = Parameter.getValue(source=values, key='install')
        service.install_username = Parameter.getValue(source=values, key='install_username')
        service.install_password = Parameter.getValue(source=values, key='install_password')
    return Response.success(Service().save(model=service, user_id=1))
