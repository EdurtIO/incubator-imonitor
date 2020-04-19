#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-17 01:18:25
# @Desc    : 主机表单脚本
# @File    : form_settings.py

from db.models import User
from flask_wtf import FlaskForm
from imforms.validators.validator_repeat import ValidatorEmailRepeat
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, EqualTo


class SettingsProfileForm(FlaskForm):
    username = StringField(u'名称')
    email = StringField(u'电子邮件', validators=[ValidatorEmailRepeat()])
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


class SettingsSecurityForm(FlaskForm):
    old_password = StringField(u'旧密码')
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, message='请输入有效的密码至少6位及以上')])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='两次输入的密码不一致')])
    submit = SubmitField(u'更新密码', render_kw={'class': 'btn btn-default', 'size': 'mini'})


class SettingsAvatarForm(FlaskForm):
    avatar = FileField(u'请选择头像', validators=[DataRequired(u'文件未选择！')])
    submit = SubmitField(u'更新头像')
