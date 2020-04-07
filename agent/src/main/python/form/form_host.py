#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 23:25:25
# @Desc    : 主机表单脚本
# @File    : models.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import Required


class HostAddForm(FlaskForm):
    hostname = StringField(u'主机名称', validators=[Required(message=u'主机名称不能为空')])
    username = StringField(u'主机账号', validators=[Required(message=u'主机账号不能为空')])
    password = PasswordField(u'主机密码')
    command = StringField(u'服务命令')
    command_start = StringField(u'服务启动命令', validators=[Required(message=u'请输入服务启动命令')])
    command_stop = StringField(u'服务停止命令', validators=[Required(message=u'请输入服务停止命令')])
    command_restart = StringField(u'服务重启命令', validators=[Required(message=u'请输入服务重启命令')])
    submit = SubmitField('添加', render_kw={'class': 'btn btn-primary', 'style': 'font-size:150%'})
