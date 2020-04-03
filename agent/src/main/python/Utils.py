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


class DirctoryUtils:

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
                value = None
        return value


if __name__ == '__main__':
    print NumberUtils().is_number('12123s')
