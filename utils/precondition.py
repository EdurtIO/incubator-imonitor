#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-26 22:36
# @File    : precondition.py
from exception.null_pointer import NullPointerException
from utils.istring import StringUtils


class Preconditions:

  @staticmethod
  def check_not_null(property=None, source=None):
    if StringUtils.is_empty(source=source):
      raise NullPointerException('''{} must not null'''.format(property))
