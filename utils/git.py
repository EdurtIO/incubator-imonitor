#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-13 22:31
# @File    : git.py
from threading import Thread

from common.state import State
from exception.null_pointer import NullPointerException
from services.service import Service
from utils.command import CommandUtils
from utils.precondition import Preconditions


class GitModel:

  def __init__(self, url=None, username=None, password=None, target=None, loggerFile=None, id=None):
    if not CommandUtils.run_command(command='git --version >> /dev/null'):
      raise NullPointerException('git not found')
    Preconditions.check_not_null(property='url', source=url)
    Preconditions.check_not_null(property='target folder', source=target)
    Preconditions.check_not_null(property='logger file', source=loggerFile)
    self.url = url
    self.username = username
    self.password = password
    self.target = target
    self.loggerFile = loggerFile
    self.id = id


def async_clone(model=GitModel):
  m = Service().find_one(id=model.id)
  try:
    CommandUtils.run_command_on_system(
      command='''echo 'execute command ||{}||' >> {}'''.format(model.command, model.loggerFile))
    flag = CommandUtils.run_command_on_system(command=model.command)
    if flag:
      m.state = State.SUCCESS.name
      CommandUtils.run_command_on_system(command='''echo 'clone status: SUCCESS' >> {}'''.format(model.loggerFile))
    else:
      m.state = State.FAILURE.name
      CommandUtils.run_command_on_system(command='''echo 'clone status: FAILURE' >> {}'''.format(model.loggerFile))
  except Exception as ex:
    m.state = State.FAILURE.name
    m.message = ex
    CommandUtils.run_command_on_system(
      command='''echo clone error: '{}' >> {}'''.format(ex, model.loggerFile))
  finally:
    Service().update(model=m)
    CommandUtils.run_command_on_system(
      command='''echo '====== end clone code ======' >> {}'''.format(model.loggerFile))


class Git:

  def __init__(self, model=GitModel):
    Preconditions.check_not_null(property='git config', source=model)
    self.model = model

  def clone(self):
    CommandUtils.run_command_on_system(
      command='''echo '====== start clone code ======' >> {}'''.format(self.model.loggerFile))
    command = '''git clone --progress {} 2> {} {}'''.format(self.model.url, self.model.loggerFile, self.model.target)
    self.model.command = command
    model = Service().find_one(id=self.model.id)
    model.state = State.RUNNING.name
    Service().update(model=model)
    thread = Thread(target=async_clone, args=(self.model,))
    thread.setDaemon(True)
    thread.start()


if __name__ == '__main__':
  model = GitModel(url='https://github.com/qianmoQ/java-design-patterns.git',
                   target='/Users/shicheng/Documents/java-design-patterns',
                   loggerFile='/Users/shicheng/Documents/a.log',
                   id=1)
  git = Git(model=model)
  git.clone()
