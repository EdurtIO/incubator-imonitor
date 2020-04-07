#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:45:26
# @Desc    : host数据服务
# @File    : service_host.py

from db.models import Host


class HostService:

    def find_all(self):
        """
        查询所有数据
        :return: 数据集合
        """
        return Host().query.all()
