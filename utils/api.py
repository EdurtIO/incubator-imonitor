#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-15 00:33
# @File    : api.py
from flask import jsonify


class ApiContent:

  def to_json(self, source=[]):
    return jsonify({'result': [dict(row) for row in source]})

  def object_to_json(self, source):
    return jsonify({'content': [row.as_dict() for row in source]})
