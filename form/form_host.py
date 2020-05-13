#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 23:25:25
# @Desc    : 主机表单脚本
# @File    : from_host.py
from common.utils import StringUtils
from db.models import Host
from flask_wtf import FlaskForm
from imforms.widgets.password_field import PasswordField
from wtforms import StringField, SubmitField, SelectField, HiddenField, IntegerField, RadioField, TextAreaField
from wtforms.validators import Required


class HostForm(FlaskForm):
    id = HiddenField(u'编码')
    server_name = StringField(u'服务名称', validators=[Required(message=u'服务名称不能为空')],
                              render_kw={'placeholder': '请输入服务名称', 'size': 'mini', 'value': 'druid'})
    server_type = StringField(u'服务类型', validators=[Required(message=u'服务类型不能为空')],
                              render_kw={'placeholder': '请输入服务类型', 'size': 'mini', 'value': 'io'})
    server = SelectField('服务', choices=[
        ('historical', 'Historical'),
        ('broker', 'Broker'),
        ('overload', 'Overload'),
        ('coordinator', 'Coordinator'),
        ('middleManager', 'MiddleManager')
    ])
    hostname = StringField(u'主机名称', validators=[Required(message=u'主机名称不能为空')],
                           render_kw={'placeholder': '请输入主机名称', 'size': 'mini'})
    ssh_port = IntegerField(u'SSH端口', validators=[Required(message=u'无效的SSH端口,只能是数值类型')],
                            render_kw={'placeholder': '请输入主机SSH端口', 'size': 'mini'})
    username = StringField(u'主机账号', validators=[Required(message=u'主机账号不能为空')],
                           render_kw={'placeholder': '请输入主机账号', 'size': 'mini'})
    security = RadioField(u'登录模式', choices=[('1', '密码'), ('0', '私钥')], default='1', validators=[Required()])
    security_password = PasswordField(u'主机密码', render_kw={'placeholder': '请输入主机密码，可为空', 'size': 'mini'})
    security_key = TextAreaField(u'主机私钥', render_kw={'placeholder': '请输入主机私钥'})
    command = StringField(u'服务命令', render_kw={'placeholder': '请输入主机查询服务命令', 'size': 'mini'})
    command_start = StringField(u'启动命令', render_kw={'placeholder': '请输入主机服务启动命令，可为空', 'size': 'mini'})
    command_stop = StringField(u'停止命令', render_kw={'placeholder': '请输入主机服务停止命令，可为空', 'size': 'mini'})
    command_restart = StringField(u'重启命令', render_kw={'placeholder': '请输入主机服务重启命令，可为空', 'size': 'mini'})
    submit = SubmitField(u'添加', render_kw={'class': 'btn btn-primary', 'size': 'mini'})
    test_connection = SubmitField(u'测试连接', render_kw={'class': 'btn btn-info', 'size': 'mini'})


class BuildModelToFrom:

    def __init__(self, host=Host, form=HostForm):
        form.id.data = host.id
        form.server_name.data = host.server_name
        form.server_type.data = host.server_type
        form.server.data = host.server
        form.hostname.data = host.hostname
        form.ssh_port.data = host.ssh_port
        form.username.data = host.username
        # 回显登录模式
        if StringUtils().is_not_empty(host.key):
            form.security.data = '0'
            form.security_key.data = host.key
        else:
            form.security.data = '1'
            form.security_password.data = host.password
        form.command.data = host.command
        form.command_start.data = host.command_restart
        form.command_stop.data = host.command_stop
        form.command_restart.data = host.command_restart
