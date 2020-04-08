#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-08 18:28:49
# @Desc    : 源码编译脚本
# @File    : assets.py
from flask_assets import Environment, Bundle


def compile_auth_assets(app):
    """
    配置授权资产包
    """
    assets = Environment(app)
    assets.config['less_bin'] = '/usr/local/bin/lessc'
    Environment.auto_build = True
    Environment.debug = False
    less_bundle = Bundle('src/less/*.less',
                         filters='less',
                         output='dist/css/account.css',
                         extra={'rel': 'stylesheet/less'})
    assets.register('less_all', less_bundle)
    less_bundle.build()
