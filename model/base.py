#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-19 22:21
# @File    : base.py
from sqlalchemy.orm import class_mapper


class BaseModel:

  def as_dict(obj):
    return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c)
