#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-03 16:11:37
# @Desc    : 插件实体模型
# @File    : PluginModel.py

import calendar
import time


class FaIconModel:
    """
    OpenFaIcon数据push模型
    """

    def __init__(self):
        self.endpoint = 'localhost'
        self.metric = ''
        self.timestamp = calendar.timegm(time.gmtime())
        self.step = 60
        self.value = 0
        self.counterType = 'GAUGE'
        self.tags = ''
