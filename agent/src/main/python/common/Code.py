#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-03 18:14:14
# @Desc    : 全局编码脚本
# @File    : Code.py

import os
import yaml

from Utils import DirctoryUtils


class StatusCode:

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

        :return:
        """
        status = []
        status_temp = DirctoryUtils().get_attr_by_key(self.codes, 'status')
        print status_temp
        for s in status_temp:
            source = DirctoryUtils().get_attr_by_key(status_temp, s)
            temp = {}
            temp['name'] = DirctoryUtils().get_attr_by_key(source, 'name')
            temp['code'] = DirctoryUtils().get_attr_by_key(source, 'code')
            temp['message'] = DirctoryUtils().get_attr_by_key(source, 'message')
            status.append(temp)
        return status

    def get_codes(self):
        print self.codes
        return self.codes

    def get_code(self, key):
        """
        根据编码key获取编码
        :param key: 编码标志
        :return: 编码
        """
        try:
            return self.codes['status'][str(key).strip().lower()]
        except:
            return None


if __name__ == '__main__':
    StatusCode()
    # print StatusCode().get_codes()
