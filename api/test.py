#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-27 21:16
# @File    : test.py
import os

from flask import Blueprint, jsonify

from application_config import application

TestApi = Blueprint('TestApi', __name__, template_folder='templates')


@TestApi.route('', methods=['GET'])
def index():
  return jsonify({'result': os.path.dirname(application.instance_path)})
