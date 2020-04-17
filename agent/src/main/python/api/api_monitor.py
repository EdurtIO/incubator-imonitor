#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-18 02:27:40
# @Desc    : 服务监控脚本
# @File    : api_monitor.py
from common.monitor import MonitorUtils
from flask import Blueprint, jsonify
from flask_login import login_required
from services.service_host import HostService

monitor_api = Blueprint('monitor_api', __name__, template_folder='templates')


@monitor_api.route('/host/<int:host_id>/network-io', methods=['GET'])
@login_required
def host_memory(host_id=int):
    host = HostService().find_one(id=host_id)
    return jsonify(
        {'result': [row.as_dict() for row in
                    MonitorUtils().network_io(hostname=host.hostname, username=host.username, password=host.password)]})
