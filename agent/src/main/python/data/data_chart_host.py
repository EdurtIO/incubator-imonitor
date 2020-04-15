#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-15 15:27:30
# @Desc    : 数据报表脚本
# @File    : chart_data.py
from datetime import datetime
from flask import Blueprint
from flask_login import login_required
from pyecharts import options as opts
from pyecharts.charts import Line

from services.service_monitor_memory import MonitorMemoryService

chart_host_data = Blueprint('chart_host_data', __name__, template_folder='templates')


@chart_host_data.route('/host/<int:host_id>/memory/rate', methods=['GET'])
@login_required
def report(host_id=int):
    chart_data = MonitorMemoryService().find_top_rate(host_id, 10)
    line = Line()
    line.add_xaxis([row[1] for row in chart_data])
    line.add_yaxis(
        "使用率(%)",
        [round(row[0] * 100, 2) for row in chart_data]
    )
    line.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=-40)
        ),
        yaxis_opts=opts.AxisOpts(
            max_=100
        ),
        legend_opts=opts.LegendOpts(is_show=False)
    )
    return line.dump_options_with_quotes()
