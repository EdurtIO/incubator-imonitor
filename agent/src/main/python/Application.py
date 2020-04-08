#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 14:25:25
# @Desc    : web程序入口脚本
# @File    : Application.py
import datetime
import json
from flask import render_template
from flask_apscheduler import APScheduler

from ImonitorService import MonitorService
from application_config import app
from push import FaIconPush
from services.service_host import HostService

# 注册自定义视图
from views.view_host import host_view

app.register_blueprint(host_view, url_prefix='/host')


class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'monitor_service_heartbeat',
            'func': '__main__:monitor_service_heartbeat',
            # 'args': (1, 2),
            'trigger': 'interval',
            'seconds': 60,
            'max_instances': 1
        }
    ]


app.config.from_object(SchedulerConfig())


def monitor_service_heartbeat():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print 'push time {}, push response {}'.format(now,
                                                  FaIconPush.FaIcon().push(json.dumps(MonitorService().service_info())))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', heartbeats=MonitorService().service_info(HostService().find_all()))


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    print app.url_map
    app.run(host='0.0.0.0', port=5000, debug=True)
