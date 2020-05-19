#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-19 23:13
# @File    : utils_parameter.py
from application_config import logger


class Parameter:

  @staticmethod
  def getValue(source=None, key=None):
    logger.debug('get value by source, key is %s', key)
    if source is None or key is None:
      return None
    try:
      return source[key]
    except Exception as ex:
      logger.error('get value error key is <%s>, reason %s', key, ex)
      return None
