#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-13 22:31
# @File    : git.py
from threading import Thread

from exception.null_pointer import NullPointerException
from utils.command import CommandUtils
from utils.precondition import Preconditions


def async_clone(model=None):
  CommandUtils.run_command_on_system(
    command='''echo '====== start clone code ======' >> {}'''.format(model.loggerFile))
  CommandUtils.run_command_on_system(
    command='''echo 'execute command ||{}||' >> {}'''.format(model.command, model.loggerFile))
  flag = CommandUtils.run_command_on_system(command=model.command)
  if flag:
    CommandUtils.run_command_on_system(command='''echo 'clone status: SUCCESS' >> {}'''.format(model.loggerFile))
  else:
    CommandUtils.run_command_on_system(command='''echo 'clone status: FAILURE' >> {}'''.format(model.loggerFile))
  return flag


class GitModel:

  def __init__(self, url=None, username=None, password=None, target=None, loggerFile=None):
    if not CommandUtils.run_command(command='git --version'):
      raise NullPointerException('git not found')
    Preconditions.check_not_null(property='url', source=url)
    Preconditions.check_not_null(property='target folder', source=target)
    Preconditions.check_not_null(property='logger file', source=loggerFile)
    self.url = url
    self.username = username
    self.password = password
    self.target = target
    self.loggerFile = loggerFile


class Git:

  def __init__(self, model=GitModel):
    Preconditions.check_not_null(property='git config', source=model)
    self.model = model

  def clone(self):
    command = '''git clone --progress {} 2> {} {}'''.format(self.model.url, self.model.loggerFile, self.model.target)
    self.model.command = command
    thread = Thread(target=async_clone, args=(self.model,))
    thread.setDaemon(True)
    thread.start()
    pass

  def a(self):
    print(1)
    CommandUtils.run_command_on_system(
      command='''echo '====== end clone code ======' >> {}'''.format(self.model.loggerFile))


if __name__ == '__main__':
  model = GitModel(url='https://github.com/qianmoQ/java-design-patterns.git',
                   target='/Users/shicheng/Documents/java-design-patterns',
                   loggerFile='/Users/shicheng/Documents/a.log')
  git = Git(model=model)
  git.clone()
