#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-03 18:14:14
# @Desc    : 全局编码脚本
# @File    : Code.py

import os
import yaml

from Utils import DirctoryUtils


class CommonCodes:

    def __init__(self):
        file_name = 'code.yaml'
        path = os.path.join(os.path.dirname(__file__).replace('common', 'config'), file_name)
        file = None
        try:
            file = open(path, 'r')
            self.codes = yaml.load(file, Loader=yaml.FullLoader)
            self.load_config()
        finally:
            if file is not None:
                file.close()

    def load_config(self):
        """
        加载系统配置文件
        :return: 配置信息
        """
        status = []
        for s in self.codes:
            status_temp = DirctoryUtils().get_attr_by_key(self.codes, s)
            for s2 in status_temp:
                source = DirctoryUtils().get_attr_by_key(status_temp, s2)
                temp = {}
                temp['name'] = DirctoryUtils().get_attr_by_key(source, 'name')
                temp['code'] = DirctoryUtils().get_attr_by_key(source, 'code')
                temp['message'] = DirctoryUtils().get_attr_by_key(source, 'message')
                temp['context'] = DirctoryUtils().get_attr_by_key(source, 'context')
                temp['operation'] = DirctoryUtils().get_attr_by_key(source, 'operation')
                temp['type'] = DirctoryUtils().get_attr_by_key(source, 'type')
                temp['parent'] = s
                status.append(temp)
        return status


if __name__ == '__main__':
    codes = CommonCodes().load_config()
    for s in codes:
        print s['message']
    # 列表解析
    print [val for val in codes if val['message'].encode('utf-8') == '宕机'][0]['message']
