#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-17 01:18:25
# @Desc    : 主机表单脚本
# @File    : form_settings.py

from db.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField


class SettingsProfileForm(FlaskForm):
    username = StringField(u'名称')
    email = StringField(u'电子邮件')
    description = TextAreaField(u'描述信息')
    website = StringField(u'网址')
    position = StringField(u'位置')
    submit = SubmitField(u'更新个人信息', render_kw={'class': 'btn btn-success', 'size': 'mini'})


class BuildModelToFrom:

    def __init__(self, user=User, form=SettingsProfileForm):
        form.username.data = user.name
        form.email.data = user.email
        form.description.data = user.description
        form.position.data = user.position
        form.website.data = user.website
