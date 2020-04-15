#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-13 17:12:42
# @Desc    : 远程连接脚本
# @File    : ssh_terminal.py

import asyncio
import threading
from tornado.websocket import WebSocketHandler

from services.service_host import HostService
from .ssh import Ssh


class SshTerminalHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def initialize(self, *args, **kwargs):
        print('Welcome To iMonitor Web Terminal')
        print(args, kwargs)

    def _reading(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            data = self.ssh.read()
            self.write_message(data)

    def open(self, *args, **kwargs):
        if args:
            server_id = int(args[0])
            host = HostService().find_one(server_id)
            self.ssh = Ssh(host=host.hostname, port=22, user=host.username, password=host.password, key_file=None,
                           passphrase=None)
            t = threading.Thread(target=self._reading)
            t.setDaemon(True)
            t.start()

    def on_message(self, message):
        if message.startswith("size"):
            cols, rows = message.split(':')[1].split(',')
            self.ssh.resize(int(cols), int(rows))
        else:
            self.ssh.send(message)

    def on_close(self):
        print("WebSocket Closed")
