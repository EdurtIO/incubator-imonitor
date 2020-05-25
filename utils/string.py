#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-25 22:24
# @File    : string.py
class StringUtils:

  @staticmethod
  def is_empty(source=None):
    """
    Determines if the string is empty
    :param source: source str
    :return: if null return true else false
    """
    return source is None or source == ''

  @staticmethod
  def is_not_empty(source):
    return not StringUtils.is_empty(source=source)
