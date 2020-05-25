#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-13 22:31
# @File    : git.py

from exception.null_pointer import NullPointerException
from utils.command import CommandUtils
from utils.string import StringUtils


class GitModel:

  def __init__(self, url=None, username=None, password=None, target=None):
    if not CommandUtils.run_command(command='git --version'):
      raise NullPointerException('git not found')
    if StringUtils.is_empty(source=url):
      raise NullPointerException('url must not null')
    if StringUtils.is_empty(source=target):
      raise NullPointerException('target folder must not null')
    self.url = url
    self.username = username
    self.password = password
    self.target = target


class Git:

  def __init__(self, model=GitModel):
    self.model = model

  def clone(self):
    pass


if __name__ == '__main__':
  model = GitModel(url='https://github.com/meanstrong/pydelo', target='/Users/shicheng/Documents')
  git = Git(model=model)
  git.clone()
