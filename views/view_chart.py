#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-13 18:27:03
# @Desc    : 数据报表脚本
# @File    : view_chart.py
from flask import render_template, Blueprint
from flask_login import login_required

chart_view = Blueprint('chart_view', __name__, template_folder='templates')


@chart_view.route('/host/<int:host_id>/report', methods=['GET'])
@login_required
def report(host_id=int):
    return render_template('chart/chart.html', host_id=host_id, title='主机监控报表')
