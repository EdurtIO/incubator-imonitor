#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:09:04
# @Desc    : 实体类
# @File    : Models.py
import datetime
from application_config import db


class Message(db.Model):
    """
    系统消息实体类
    """
    __tablename__ = 'message'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    context = db.Column(db.Text, nullable=False)
    operation = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    parent = db.Column(db.String(100), nullable=False)


class Host(db.Model):
    """
    主机实体类
    """
    __tablename__ = 'host'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hostname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    command = db.Column(db.String(255), nullable=False)
    command_start = db.Column(db.String(255), nullable=False)
    command_stop = db.Column(db.String(255), nullable=False)
    command_restart = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    # active = db.Column(db.Boolean, nullable=False, server_default=True, comment='激活状态，默认为激活（True）')


db.create_all()
