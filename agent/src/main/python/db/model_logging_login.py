#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-18 03:18:04
# @Desc    : 登录日志
# @File    : model_logging_login.py
import datetime

from application_config import db


class LoginLogging(db.Model):
    __tablename__ = 'logging_login'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_time = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now, comment='登录时间')
    position = db.Column(db.String(100), nullable=True, comment='登录地址')
    ip = db.Column(db.String(100), nullable=True, comment='登录IP')
    client = db.Column(db.String(100), nullable=True, comment='客户端')
    status = db.Column(db.Boolean, nullable=True, comment='登录状态')
    reason = db.Column(db.String(100), nullable=True, comment='失败原因')


db.create_all()
