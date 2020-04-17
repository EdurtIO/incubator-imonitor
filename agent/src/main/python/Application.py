#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 14:25:25
# @Desc    : web程序入口脚本
# @File    : Application.py
import datetime
from ImonitorService import MonitorService
from application_config import app, codes
from flask import render_template
from flask_apscheduler import APScheduler
# 注册自定义视图
from views.view_auth import auth_view
from views.view_chart import chart_view
from views.view_dashboard import dashboard_view
from views.view_host import host_view
from views.view_terminal import terminal_view
from views.view_settings import settings_view

app.register_blueprint(host_view, url_prefix='/host')
app.register_blueprint(auth_view, url_prefix='/auth')
app.register_blueprint(dashboard_view, url_prefix='/dashboard')
app.register_blueprint(terminal_view, url_prefix='/terminal')
app.register_blueprint(chart_view, url_prefix='/chart')
app.register_blueprint(settings_view, url_prefix='/settings')

from api.api_chart import chart_api
from api.api_monitor import monitor_api

app.register_blueprint(chart_api, url_prefix='/api/chart')
app.register_blueprint(monitor_api, url_prefix='/api/monitor')


from data.data_chart_host import chart_host_data

app.register_blueprint(chart_host_data, url_prefix='/data/chart')

## 启用websocket服务
from common.ssh_terminal import SshTerminalHandler
from tornado.web import FallbackHandler, Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

app_wsgi = WSGIContainer(app)
handlers = [
    (r"/websocket/(.*)", SshTerminalHandler, {}),  # {'term_manager': term_manager}),
    (r"/(.*)", FallbackHandler, dict(fallback=app_wsgi))
]

application = Application(handlers, debug=True)


class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'monitor_service_heartbeat',
            'func': '__main__:monitor_service_heartbeat',
            # 'args': (1, 2),
            'trigger': 'interval',
            'seconds': 300,
            'max_instances': 1
        }
    ]


app.config.from_object(SchedulerConfig())

from services.service_monitor_memory import MonitorMemoryService
from services.service_monitor_cpu import MonitorCpuService
from common.monitor import MonitorUtils

from services.service_host import HostService


def monitor_service_heartbeat():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now)
    for host in HostService().find_all():
        memory = MonitorUtils().memory(host.username, host.hostname, host.password)
        if memory is not None:
            MonitorMemoryService().add(memory, host.id)
        cpu = MonitorUtils().cpu(host.username, host.hostname, host.password)
        if cpu is not None:
            MonitorCpuService().add(monitor_cpu=cpu, host_id=host.id)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', heartbeats=MonitorService().service_info(HostService().find_all()))


@app.errorhandler(404)
def handle_404_error(err_msg):
    return render_template('404.html', error=err_msg)


@app.errorhandler(500)
def handle_404_error(err_msg):
    return render_template('500.html', error=err_msg)


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    print(app.url_map)
    httpserver = HTTPServer(application)
    # app.run(host='0.0.0.0', port=codes['server']['port'], debug=codes['server']['debug'])
    httpserver.listen(port=int(codes['server']['port']))
    IOLoop.current().start()
