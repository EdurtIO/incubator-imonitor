#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-25 22:57
# @File    : command.py
import subprocess

from utils.string import StringUtils


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


if __name__ == '__main__':
  print(CommandUtils.run_command(command='git --version'))
