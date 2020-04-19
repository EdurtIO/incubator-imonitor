#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-01 15:21:25
# @Desc    : 服务器应用进程监控脚本
# @File    : ImonitorService.py

import calendar
import json
import time

from Config import ConfigUtils
from common.code import CommonCodes
from common.utils import CommandUtils
from common.utils import NumberUtils


class MonitorService:

    def __init__(self):
        self.config = ConfigUtils().build_agent_configs()
        self.messages = CommonCodes().load_config()

    def service_info(self, datas):
        """
        获取服务信息
        :return: 服务信息
        """
        heartbeats = []
        try:
            for host in datas:
                if host.command is None or host.command == '':
                    command = ConfigUtils().get_command(service_name=host.server, service_type=host.server_type,
                                                        cluster_name=host.server_name)
                    if command is not None:
                        host.command = command.command
            if host is not None and host.command is not None:
                buffer = CommandUtils().command_ssh_remote(user=host.username,
                                                           host=host.hostname,
                                                           password=host.password,
                                                           command=host.command)
                # print '-------------------华丽的分割线---------------------'
                service_heartbeat = buffer.before.split()
                heartbeat = {}
                heartbeat['service_name'] = host.server
                heartbeat['service_username'] = service_heartbeat[0]
                heartbeat['service_pid'] = service_heartbeat[1]
                heartbeat['service_host'] = host.hostname
                heartbeat['service_timestamp'] = calendar.timegm(time.gmtime())
                service_status = 'DOWN'
                if NumberUtils().is_number(service_heartbeat[1]):
                    service_status = 'UP'
                    heartbeat['service_code'] = '2000'
                else:
                    heartbeat['service_pid'] = '-'
                    heartbeat['service_context'] = buffer.before
                    message = [v for v in self.messages if v['context'] is not None and buffer.before.find(v['context'].encode('utf-8')) >= 0]
                    if message is not None and len(message) > 0:
                        heartbeat['service_message'] = message[0]['message']
                        heartbeat['service_code'] = str(message[0]['code'])
                    else:
                        heartbeat['service_code'] = '2000'
                    heartbeat['service_username'] = '-'
                heartbeat['service_status'] = service_status
                heartbeats.append(heartbeat)
        except Exception as ex:
            pass

        # 读取配置文件
        # for monitor in self.config:
        #     service_names = monitor.id.split('_')
        #     for host in monitor.hosts:
        #         if host.command is None:
        #             command = ConfigUtils().get_command(service_name=service_names[2], service_type=monitor.type,
        #                                                 cluster_name=monitor.name)
        #             if command is not None:
        #                 host.command = command.command
        #         if host is not None and host.command is not None:
        #             buffer = RemoteCommand.command_ssh_remote(user=host.username,
        #                                                       host=host.host,
        #                                                       password=host.password,
        #                                                       command=host.command)
        #             # print '-------------------华丽的分割线---------------------'
        #             service_heartbeat = buffer.before.split()
        #             heartbeat = {}
        #             heartbeat['service_name'] = service_names[2]
        #             heartbeat['service_username'] = service_heartbeat[0]
        #             heartbeat['service_pid'] = service_heartbeat[1]
        #             heartbeat['service_host'] = host.host
        #             heartbeat['service_timestamp'] = calendar.timegm(time.gmtime())
        #             service_status = 'DOWN'
        #             if NumberUtils().is_number(service_heartbeat[1]):
        #                 service_status = 'UP'
        #                 heartbeat['service_code'] = '2000'
        #             else:
        #                 heartbeat['service_pid'] = '-'
        #                 heartbeat['service_context'] = buffer.before
        #                 message = [v for v in self.messages if buffer.before.find(str(v['context'])) >= 0]
        #                 if message is not None and len(message) > 0:
        #                     heartbeat['service_message'] = message[0]['message'].encode('utf-8')
        #                     heartbeat['service_code'] = str(message[0]['code'])
        #                 else:
        #                     heartbeat['service_code'] = '2000'
        #                 heartbeat['service_username'] = '-'
        #             heartbeat['service_status'] = service_status
        #             heartbeats.append(heartbeat)
        return heartbeats


if __name__ == '__main__':
    print(json.dumps(MonitorService().service_info()))
