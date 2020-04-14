#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-13 18:27:03
# @Desc    : 数据报表脚本
# @File    : view_chart.py
from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required
from jinja2 import Markup

from services.service_monitor_memory import MonitorMemoryService

from common.monitor import MonitorUtils

from pyecharts import options as opts
from pyecharts.charts import Line

chart_view = Blueprint('chart_view', __name__, template_folder='templates')


@chart_view.route('/host/<int:host_id>/memory', methods=['GET'])
@login_required
def host_memory(host_id=int):
    chart = MonitorMemoryService().find_top_15(host_id)
    c = (Line()
         .add_xaxis([row[9] for row in chart])
         # .add_yaxis("空闲内存", [row[1] for row in chart])
         # .add_yaxis("文件缓冲", [row[2] for row in chart])
         .add_yaxis("使用率", [row[8] for row in chart])
         .set_global_opts(title_opts=opts.TitleOpts(title="主机内存监控报表", subtitle="单位%（间隔时间5秒）"))
         )
    return Markup(c.render_embed())
    # return render_template('chart/chart.html', server_id=host_id, charts=chart)
