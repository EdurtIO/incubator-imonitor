#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-19 19:16:04
# @Desc    : 命令执行历史
# @File    : model_command_execute.py
import datetime

from application_config import db


class CommandExecute(db.Model):
    __tablename__ = 'command_execute'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command = db.Column(db.Text, nullable=True, comment='执行命令')
    final_state = db.Column(db.Boolean, nullable=True, default=False, comment='最终执行状态')
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='执行开始时间')
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='执行结束时间')
    elapsed_time = db.Column(db.BigInteger, nullable=False, default=datetime.datetime.now, comment='执行耗时')
    reason = db.Column(db.String(100), nullable=True, comment='失败原因')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')


db.create_all()
