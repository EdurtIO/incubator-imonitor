#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-13 23:43
# @File    : common.py
import os

from application_config import logger


class Common:

  def create_folder(self, dest):
    logger.info('create target folder <%s> start', dest)
    if dest is not None:
      if os.path.exists(dest) is False:
        os.makedirs(dest)
      logger.info('create folder <%s> success', dest)
    else:
      logger.error('target folder <%s> error')
