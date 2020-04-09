#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-09 10:49:39
# @Desc    : 仪表盘脚本
# @File    : view_dashboard.py
from flask import render_template, Blueprint
from flask_login import login_required

from services.service_host import HostService

dashboard_view = Blueprint('dashboard_view', __name__, template_folder='templates')


@dashboard_view.route('/', methods=['GET'])
@login_required
def index():
    count = HostService().count_by_user()
    return render_template('dashboard/dashboard-index.html', title='仪表盘', count=count)
