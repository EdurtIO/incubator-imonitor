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

    def print_json(self):
        print json.dumps(self, lambda obj: obj.__dict__)


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


class ConfigUtils:

    def __init__(self):
        file = open('agent.yaml')
        self.content = yaml.load(file, Loader=yaml.FullLoader)
        file.close()

    def build_configs(self):
        """
        解析配置文件处理监控数据部分
        :return: 配置信息集合
        """
        models = []
        rules = self.content['rules']
        for temp in rules:
            rule = rules[temp]
            model = ConfigModel()
            model.id = temp
            model.type = rule['type']
            model.name = rule['name']
            # 解析主机信息部分
            temp_hosts = rule['hosts']
            hosts = []
            for h in temp_hosts:
                host = temp_hosts[h]
                model_host = ConfigHostModel()
                model_host.id = h
                model_host.host = host['host']
                model_host.username = host['username']
                model_host.password = host['password']
                hosts.append(model_host)
            model.hosts = hosts
            model.message = rule['message']
            models.append(model)
        return models


if __name__ == '__main__':
    for model in ConfigUtils().build_configs():
        model.print_json()
