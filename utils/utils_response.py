#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-19 23:32
# @File    : utils_response.py
from flask import jsonify


class Response:

  @staticmethod
  def success(status=None):
    if status is None:
      status = False
    return jsonify({
      'code': 2000,
      'content': status
    })
