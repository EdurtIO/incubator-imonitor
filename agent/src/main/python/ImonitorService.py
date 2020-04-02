#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-01 15:21:25
# @Desc    : 服务器应用进程监控脚本
# @File    : ImonitorService.py

import calendar
import time

import RemoteCommand
from Config import ConfigUtils
from Utils import NumberUtils


class MonitorService:

    def __init__(self):
        self.config = ConfigUtils().build_agent_configs()

    def service_info(self):
        heartbeats = []
        """
        获取服务信息
        :return: 服务信息
        """
        for monitor in self.config:
            service_names = monitor.id.split('_')
            for host in monitor.hosts:
                if host.command is None:
                    command = ConfigUtils().get_command(service_name=service_names[2], service_type=monitor.type,
                                                        cluster_name=monitor.name)
                    if command is not None:
                        host.command = command.command
                if host is not None and host.command is not None:
                    buffer = RemoteCommand.command_ssh_remote(user=host.username,
                                                              host=host.host,
                                                              password=host.password,
                                                              command=host.command)
                    # print '-------------------华丽的分割线---------------------'
                    service_heartbeat = buffer.before.split()
                    heartbeat = {}
                    heartbeat['service_name'] = service_names[2]
                    heartbeat['service_username'] = service_heartbeat[0]
                    heartbeat['service_pid'] = service_heartbeat[1]
                    heartbeat['service_host'] = host.host
                    heartbeat['service_timestamp'] = calendar.timegm(time.gmtime())
                    service_status = 'DOWN'
                    if NumberUtils().is_number(service_heartbeat[1]):
                        service_status = 'UP'
                    else:
                        heartbeat['service_pid'] = '-'
                        heartbeat['message'] = buffer.before
                    heartbeat['service_status'] = service_status
                    heartbeats.append(heartbeat)
        return heartbeats


if __name__ == '__main__':
    MonitorService().service_info()
