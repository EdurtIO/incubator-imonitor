#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-15 14:12:40
# @Desc    : 数据报表脚本
# @File    : api_chart.py
from flask import Blueprint, jsonify
from flask_login import login_required

from services.service_monitor_memory import MonitorMemoryService

chart_api = Blueprint('chart_api', __name__, template_folder='templates')


@chart_api.route('/host/<int:host_id>/memory', methods=['GET'])
@login_required
def host_memory(host_id=int):
    charts = MonitorMemoryService().find_top_15(host_id)
    return jsonify({'result': [dict(row) for row in charts]})

