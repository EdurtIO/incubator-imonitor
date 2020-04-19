#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-13 17:12:42
# @Desc    : 远程连接脚本
# @File    : ssh_terminal.py

import asyncio
import datetime
import threading
from application_config import logger
from db.model_command_execute import CommandExecute
from services.service_command_execute import CommandExecuteService
from services.service_host import HostService
from services.service_user import UserService
from tornado.websocket import WebSocketHandler

from .ssh import Ssh


class SshTerminalHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def initialize(self, *args, **kwargs):
        logger.info('Welcome To iMonitor Web Terminal')
        logger.info('login in params <%s>, kwargs <%s>', args, kwargs)

    def open(self, *args, **kwargs):
        if args:
            server_id = int(args[0])
            user_id = int(args[1])
            self.host = HostService().find_one(id=server_id)
            self.command = ''
            self.persistence = False
            self.user = UserService().find_one(id=user_id)
            self.user_id = user_id
            self.host_id = server_id
            self.end_time = datetime.datetime.now()
            self.start_time = datetime.datetime.now()
            self.reason = ''
            logger.info('connected from <%s> by <%s> start', self.host.hostname, self.host.username)
            self.ssh = Ssh(hostname=self.host.hostname, port=self.host.ssh_port, username=self.host.username,
                           password=self.host.password, private_key=self.host.key)
            t = threading.Thread(target=self._reading)
            t.setDaemon(True)
            t.start()

    def _reading(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.finalState = False
        while True:
            if self.ssh.connected:
                context = self.ssh.read()
                if context.decode().strip() is '':
                    self.end_time = datetime.datetime.now()
                    # 确保回车后的执行命令
                    self.finalState = True
                    execute = self.build()
                    if CommandExecuteService().add(model=execute, user_id=self.user_id, host_id=self.host_id):
                        self.command = ''
                self.write_message(context)
            else:
                reason = 'connected from <%s> by <%s> failure'.format(self.ssh.hostname, self.ssh.username)
                logger.error(reason)
                self.finalState = False
                self.reason = reason
                self.end_time = datetime.datetime.now()
                execute = self.build()
                if CommandExecuteService().add(model=execute, user_id=self.user_id, host_id=self.host_id):
                    self.command = ''
                break


    def on_message(self, message):
        if message.startswith("size"):
            cols, rows = message.split(':')[1].split(',')
            self.ssh.resize(int(cols), int(rows))
        else:
            if self.ssh.connected:
                self.persistence = False
                if message is not '\r':
                    self.command += message
                if message is '\r':
                    # 记录键盘回车后的执行命令，确保持久化数据
                    self.persistence = True
                    self.start_time = datetime.datetime.now()
                self.ssh.send(message)
            else:
                logger.error('not connected from <%s> by <%s>', self.ssh.hostname, self.ssh.username)
                raise Exception('connected closed')

    def build(self):
        execute = CommandExecute()
        execute.command = self.command
        execute.final_state = self.finalState
        execute.start_time = self.start_time
        execute.end_time = self.end_time
        execute.elapsed_time = (self.end_time - self.start_time).microseconds
        execute.reason = self.reason
        return execute

    def on_close(self):
        logger.info('socket closed from <%s> by <%s>', self.ssh.hostname, self.ssh.username)
