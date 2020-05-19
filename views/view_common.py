#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-13 23:15
# @File    : view_common.py

from flask import Blueprint, render_template

CommonView = Blueprint('CommonView', __name__, template_folder='templates')


@CommonView.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html', heartbeats=[])


@CommonView.errorhandler(404)
def handle_404_error(err_msg):
  return render_template('404.html', error=err_msg)


@CommonView.errorhandler(500)
def handle_404_error(err_msg):
  return render_template('500.html', error=err_msg)
