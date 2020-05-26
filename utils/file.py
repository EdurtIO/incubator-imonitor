#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-26 22:51
# @File    : file.py
from utils.precondition import Preconditions


class FileUtils:

  @staticmethod
  def create_file(file=str):
    Preconditions.check_not_null(property='file', source=file)


if __name__ == '__main__':
  FileUtils.create_file(file=None)
