#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 16:30:15
# @Desc    : 全局工具类脚本
# @File    : Utils.py


class NumberUtils:

    def is_number(self, content):
        """
        判断数据是否是数值类型
        :param content: 数据
        :return: True|False
        """
        if content is None:
            return False
        try:
            float(content)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    print NumberUtils().is_number('12123s')
