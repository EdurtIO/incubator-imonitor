#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-01 18:25:25
# @Desc    : 配置文件处理脚本
# @File    : Config.py

import json
import yaml


class ConfigHostModel:
    """
    监控信息主机实体
    """

    def __init__(self):
        self.id = ''
        self.host = ''
        self.username = ''
        self.password = ''
        self.command = ''

    def print_json(self):
        print json.dumps(self.__dict__)


class ConfigModel:
    """
    监控信息实体
    """

    def __init__(self):
        self.id = ''  # 服务ID
        self.name = ''  # 服务名称
        self.type = ''  # 服务类型
        self.hosts = [ConfigHostModel]  # 主机
        self.message = ''  # 提示信息

    def print_json(self):
        print json.dumps(self.__dict__)


class ServiceCommandModel:
    """
    服务命令实体
    """

    def __init__(self):
        self.id = ''  # 服务ID
        self.name = ''  # 服务名称
        self.type = ''  # 服务类型
        self.commands = []  # 命令

    def print_json(self):
        print json.dumps(self.__dict__)


class ConfigUtils:

    def __init__(self):
        file_agent = open('agent.yaml', 'r')
        self.content_agent = yaml.load(file_agent, Loader=yaml.FullLoader)
        file_agent.close()
        file_command = open('service_command.yaml', 'r')
        self.content_command = yaml.load(file_command, Loader=yaml.FullLoader)
        file_command.close()

    def get_attr_by_key(self, content, key):
        """
        根据提供的key获取属性值
        :param content: 源数据
        :param key: key
        :return: 属性值，默认为None
        """
        value = None
        if key is '':
            print '无效的主键'
        else:
            try:
                value = content[key]
            except Exception:
                # print '无效的主键数据设置为None'
                value = None
        return value

    def build_agent_configs(self):
        """
        解析探针配置文件处理监控数据
        :return: 探针配置信息集合
        """
        models = []
        rules = self.content_agent['rules']
        for temp in rules:
            rule = self.get_attr_by_key(content=rules, key=temp)
            model = ConfigModel()
            model.id = temp
            model.type = self.get_attr_by_key(content=rule, key='type')
            model.name = self.get_attr_by_key(content=rule, key='name')
            # 解析主机信息部分
            temp_hosts = self.get_attr_by_key(content=rule, key='hosts')
            hosts = []
            for h in temp_hosts:
                host = self.get_attr_by_key(content=temp_hosts, key=h)
                model_host = ConfigHostModel()
                model_host.id = h
                model_host.host = self.get_attr_by_key(content=host, key='host')
                model_host.username = self.get_attr_by_key(content=host, key='username')
                model_host.password = self.get_attr_by_key(content=host, key='password')
                model_host.command = self.get_attr_by_key(content=host, key='command')
                hosts.append(model_host)
            model.hosts = hosts
            model.message = self.get_attr_by_key(content=rule, key='message')
            models.append(model)
        return models

    def build_command_configs(self):
        """
        解析默认服务命令配置数据
        :return: 默认服务配置信息
        """
        models = []
        commands = self.content_command
        for command_temp in commands:
            service_command = ServiceCommandModel()
            command = self.get_attr_by_key(content=commands, key=command_temp)
            service_command.id = command_temp
            service_command.name = self.get_attr_by_key(content=command, key='name')
            service_command.type = self.get_attr_by_key(content=command, key='type')
            command_services = self.get_attr_by_key(content=command, key='commands')
            command_temps = []
            if command_services is not None:
                for command_service in self.get_attr_by_key(content=command, key='commands'):
                    temp = self.get_attr_by_key(content=command_services, key=command_service)
                    c = {}
                    c['id'] = command_service
                    c['name'] = self.get_attr_by_key(content=temp, key='name')
                    c['command'] = self.get_attr_by_key(content=temp, key='command')
                    print c
                    command_temps.append(c)
            service_command.commands = command_temps
            models.append(service_command)
        return models


if __name__ == '__main__':
    for model in ConfigUtils().build_command_configs():
        print '-------------------华丽的分割线---------------------'
        print
        print model.id
        print model.name
        print model.type
        print model.commands
        print

    for model in ConfigUtils().build_agent_configs():
        for host in model.hosts:
            host.print_json()
