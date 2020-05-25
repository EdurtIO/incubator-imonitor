#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-25 22:44
# @File    : null_pointer.py

class NullPointerException(Exception):

  def __init__(self, *args):
    self.args = args
