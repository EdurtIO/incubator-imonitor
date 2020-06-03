#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-06-03 22:32
# @File    : state.py
from enum import Enum


class State(Enum):
  INITED = 'Inited'
  RUNNING = 'Running'
  SUCCESS = 'Success'
  FAILURE = 'Failure'
