#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-13 17:12:42
# @Desc    : 远程连接脚本
# @File    : ssh_terminal.py

import asyncio
import threading
from application_config import logger
from services.service_host import HostService
from tornado.websocket import WebSocketHandler

from .ssh import Ssh


class SshTerminalHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def initialize(self, *args, **kwargs):
        logger.info('Welcome To iMonitor Web Terminal')
        logger.info('login in params <%s>, kwargs <%s>', args, kwargs)

    def _reading(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            if self.ssh.connected:
                data = self.ssh.read()
                self.write_message(data)
            else:
                logger.error('connected from <%s> by <%s> failure', self.ssh.hostname, self.ssh.username)
                break

    def open(self, *args, **kwargs):
        if args:
            server_id = int(args[0])
            host = HostService().find_one(server_id)
            self.ssh = Ssh(hostname=host.hostname, port=host.ssh_port, username=host.username, password=host.password,
                           private_key=host.key)
            t = threading.Thread(target=self._reading)
            t.setDaemon(True)
            t.start()

    def on_message(self, message):
        if message.startswith("size"):
            cols, rows = message.split(':')[1].split(',')
            self.ssh.resize(int(cols), int(rows))
        else:
            if self.ssh.connected:
                self.ssh.send(message)
            else:
                logger.error('not connected from <%s> by <%s>', self.ssh.hostname, self.ssh.username)
                raise Exception('connected closed')

    def on_close(self):
        logger.info('socket closed from <%s> by <%s>', self.ssh.hostname, self.ssh.username)
