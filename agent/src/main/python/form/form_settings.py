#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-17 01:18:25
# @Desc    : 主机表单脚本
# @File    : form_settings.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SettingsProfileForm(FlaskForm):
    username = StringField(u'名称')
    email = StringField(u'电子邮件')
    description = StringField(u'描述信息')
    website = StringField(u'网址')
    position = StringField(u'位置')
    submit = SubmitField(u'更新个人信息', render_kw={'class': 'btn btn-success', 'size': 'mini'})
