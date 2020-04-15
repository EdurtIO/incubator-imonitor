#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-13 17:11:16

import os
from application_config import app
from common.ssh_terminal import SshTerminalHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, Application
from tornado.wsgi import WSGIContainer

app = WSGIContainer(app)
handlers = [
    (r"/websocket/(.*)", SshTerminalHandler, {}),  # {'term_manager': term_manager}),
    (r"/(.*)", FallbackHandler, dict(fallback=app))
]

application = Application(handlers, debug=True)

if __name__ == "__main__":
    # sp = config.secure_path
    # if sp:
    #     httpserver = HTTPServer(application, ssl_options={
    #         "certfile": os.path.join(config.secure_path, config.certfile_path),
    #         "keyfile": os.path.join(config.secure_path, config.key_path),
    #     })
    # else:
    httpserver = HTTPServer(application)
    httpserver.listen(int(2000))
    IOLoop.current().start()
