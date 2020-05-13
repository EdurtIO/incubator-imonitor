#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-13 22:31
# @File    : git.py

from application_config import configuration, logger

from utils.common import Common


class Git:

  def __init__(self, dest, url):
    if dest is None or dest == '':
      self.dest = configuration['resources']['dest']
    else:
      self.dest = dest
    if url is None:
      self.url = url
      logger.error('remote git address is not null')

  def clone(self):
    Common().create_folder(dest=self.dest)
    pass


if __name__ == '__main__':
  git = Git(dest=None, url='https://github.com/meanstrong/pydelo');
  git.clone()
