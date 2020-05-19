#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-04-02 14:25:25
# @File    : Application.py
import datetime

from flask_apscheduler import APScheduler

from application_config import application, configuration
from views.view_common import CommonView

application.register_blueprint(CommonView, url_prefix='/')

## 启用websocket服务
from common.ssh_terminal import SshTerminalHandler
from tornado.web import FallbackHandler, Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

app_wsgi = WSGIContainer(application)
handlers = [
    (r"/websocket/(.*)/(.*)", SshTerminalHandler, {}),  # {'term_manager': term_manager}),
    (r"/(.*)", FallbackHandler, dict(fallback=app_wsgi))
]

applicationServer = Application(handlers, debug=True)


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


application.config.from_object(SchedulerConfig())

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

if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(application)
    scheduler.start()
    print(application.url_map)
    httpserver = HTTPServer(applicationServer)
    # app.run(host='0.0.0.0', port=codes['server']['port'], debug=codes['server']['debug'])
    httpserver.listen(port=int(configuration['server']['port']))
    IOLoop.current().start()
