#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-25 22:57
# @File    : command.py
import os
import subprocess

from utils.precondition import Preconditions
from utils.istring import StringUtils


class CommandUtils:

  @staticmethod
  def run_command(command=None):
    if StringUtils.is_empty(source=command):
      return False
    else:
      response = subprocess.check_call(command, shell=True)
      if response == 0:
        return True
    return False

  @staticmethod
  def run_command_on_system(command=None):
    Preconditions.check_not_null(property='command', source=command)
    if os.system(command) == 0:
      return True
    else:
      return False

  @staticmethod
  def run_command_response_to_file(command=str, loggerFile=str):
    Preconditions.check_not_null(property='command', source=command)
    Preconditions.check_not_null(property='logger file', source=loggerFile)
    os.system('''{} >> {}'''.format(command, loggerFile))


if __name__ == '__main__':
  # print(CommandUtils.run_command(command='git --version'))
  CommandUtils.run_command_response_to_file(command='ls -l -a', loggerFile='/Users/shicheng/Documents/a.log')
