#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-08 15:54:15
# @Desc    : 用户授权脚本
# @File    : from_auth.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class AuthSignin(FlaskForm):
    """
    登录表单
    """
    name = StringField('账号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


class AuthSignup(FlaskForm):
    """
    注册表单
    """
    name = StringField('用户名', validators=[Length(min=6, message='请输入有效的密码至少6位及以上'), DataRequired()])
    email = StringField('邮箱', validators=[Length(min=6, message='请输入有效的密码至少6位及以上'), Email(message='请输入有效邮箱'), DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, message='请输入有效的密码至少6位及以上')])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='两次输入的密码不一致')])
    submit = SubmitField('注册')
