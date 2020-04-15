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
        print(json.dumps(self.__dict__))


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
        print(json.dumps(self.__dict__))


class ServiceCommandModel:
    """
    服务命令实体
    """

    def __init__(self):
        self.id = ''  # 服务ID
        self.name = ''  # 服务名称
        self.type = ''  # 服务类型
        self.commands = [ServiceCommandSimpleModel]  # 命令

    def print_json(self):
        print(json.dumps(self.__dict__))


class ServiceCommandSimpleModel:
    """
    服务命令实体
    """

    def __init__(self):
        self.id = ''  # 服务ID
        self.name = ''  # 服务名称
        self.command = []  # 命令

    def print_json(self):
        print(json.dumps(self.__dict__))


def get_attr_by_key(content, key):
    """
    根据提供的key获取属性值
    :param content: 源数据
    :param key: key
    :return: 属性值，默认为None
    """
    value = None
    if key is '':
        print('无效的主键')
    else:
        try:
            value = content[key]
        except Exception:
            # print('无效的主键数据设置为None')
            value = None
    return value


class ConfigUtils:

    def __init__(self):
        file_agent = open('agent.yaml', 'r')
        self.content_agent = yaml.load(file_agent)
        file_agent.close()
        file_command = open('service_command.yaml', 'r')
        self.content_command = yaml.load(file_command)
        file_command.close()

    def build_agent_configs(self):
        """
        解析探针配置文件处理监控数据
        :return: 探针配置信息集合
        """
        models = []
        rules = self.content_agent['rules']
        for temp in rules:
            rule = get_attr_by_key(content=rules, key=temp)
            model = ConfigModel()
            model.id = temp
            model.type = get_attr_by_key(content=rule, key='type')
            model.name = get_attr_by_key(content=rule, key='name')
            # 解析主机信息部分
            temp_hosts = get_attr_by_key(content=rule, key='hosts')
            hosts = []
            for h in temp_hosts:
                host = get_attr_by_key(content=temp_hosts, key=h)
                model_host = ConfigHostModel()
                model_host.id = h
                model_host.host = get_attr_by_key(content=host, key='host')
                model_host.username = get_attr_by_key(content=host, key='username')
                model_host.password = get_attr_by_key(content=host, key='password')
                model_host.command = get_attr_by_key(content=host, key='command')
                hosts.append(model_host)
            model.hosts = hosts
            model.message = get_attr_by_key(content=rule, key='message')
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
            command = get_attr_by_key(content=commands, key=command_temp)
            service_command.id = command_temp
            service_command.name = get_attr_by_key(content=command, key='name')
            service_command.type = get_attr_by_key(content=command, key='type')
            command_services = get_attr_by_key(content=command, key='commands')
            command_temps = []
            if command_services is not None:
                for command_service in get_attr_by_key(content=command, key='commands'):
                    temp = get_attr_by_key(content=command_services, key=command_service)
                    command_simple = ServiceCommandSimpleModel()
                    command_simple.id = command_service
                    command_simple.name = get_attr_by_key(content=temp, key='name')
                    command_simple.command = get_attr_by_key(content=temp, key='command')
                    command_temps.append(command_simple)
            service_command.commands = command_temps
            models.append(service_command)
        return models

    def get_command(self, service_name, service_type, cluster_name):
        """
        获取默认命名
        :param service_name: 服务名称，例如：historical
        :param service_type: 服务类型，例如：apache
        :param cluster_name: 集群类型，例如：druid
        :return: 命令想起
        """
        commands = self.build_command_configs()
        command_response = None
        for command in commands:
            if command.name.strip() == cluster_name.strip() and command.type.strip() == service_type.strip():
                if len(command.commands) > 0:
                    for command_temp in command.commands:
                        if command_temp.name.strip() == service_name.strip():
                            command_response = command_temp
        return command_response


if __name__ == '__main__':
    ConfigUtils().get_command(service_name='historical', service_type='io', cluster_name='druid')
    # for model in ConfigUtils().build_command_configs():
    #     print '-------------------华丽的分割线---------------------'
    #     print
    #     print model.id
    #     print model.name
    #     print model.type
    #     print model.commands
    #     print
    #
    # for model in ConfigUtils().build_agent_configs():
    #     for host in model.hosts:
    #         host.print_json()
