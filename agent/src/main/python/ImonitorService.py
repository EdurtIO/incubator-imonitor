#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-01 15:21:25
# @Desc    : 服务器应用进程监控脚本
# @File    : ImonitorService.py

import getpass
import pexpect
import socket
import yaml

import RemoteCommand
from Config import ConfigUtils


class MonitorService:

    def __init__(self):
        f = open('agent.yaml')
        content = yaml.load(f, Loader=yaml.FullLoader)
        self.hostname = content['application']['remote']['hostname']
        if self.hostname is None:
            self.hostname = socket.gethostname()
        self.username = content['application']['remote']['username']
        if self.username is None:
            self.username = getpass.getuser()
        self.password = content['application']['remote']['password']
        self.interval = content['application']['interval']
        self.points = content['application']['points']
        self.services = content['application']['services']
        if self.services is None:
            self.services = []
        f.close()
        print self.services

    def validate_service_status(self):
        child = RemoteCommand.command_ssh_remote(user=self.username,
                                                 host=self.hostname,
                                                 password=self.password,
                                                 command='ls -l')
        child.expect(pexpect.EOF)
        # print child


if __name__ == '__main__':
    # MonitorService().validate_service_status();
    print ConfigUtils().build_configs()
