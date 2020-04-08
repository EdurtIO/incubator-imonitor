#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-08 15:54:15
# @Desc    : 用户授权脚本
# @File    : from_auth.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class AuthSignin(FlaskForm):
    """
    登录表单
    """
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入有效的邮箱地址')])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')
