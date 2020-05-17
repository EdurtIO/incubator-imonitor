#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-15 14:12:40
# @Desc    : 数据报表脚本
# @File    : api_chart.py
from flask import Blueprint
from flask_login import current_user, login_required

from services.service_host import HostService
from utils.api import ApiContent

ApiHost = Blueprint('ApiHost', __name__, template_folder='templates')


@ApiHost.route('/list', methods=['GET'])
@login_required
def getAll():
    hosts = HostService().find_all_order_by_create_time_desc_and_user(current_user)
    return ApiContent().object_to_json(source=hosts)
