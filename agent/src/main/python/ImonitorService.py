#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-01 15:21:25
# @Desc    : 服务器应用进程监控脚本
# @File    : ImonitorService.py

import RemoteCommand
from Config import ConfigUtils


class MonitorService:

    def __init__(self):
        self.config = ConfigUtils().build_agent_configs()

    def validate_service_status(self):
        for monitor in self.config:
            print monitor.id
            for host in monitor.hosts:
                if host.command is None:
                    host.command = 'ls -l'
                buffer = RemoteCommand.command_ssh_remote(user=host.username,
                                                          host=host.host,
                                                          password=host.password,
                                                          command=host.command)
                print buffer.before
                print '-------------------华丽的分割线---------------------'
                print buffer.before.split()


if __name__ == '__main__':
    MonitorService().validate_service_status()
