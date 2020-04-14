#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:09:04
# @Desc    : 实体类
# @File    : models_monitor.py
import datetime

from application_config import db


class MonitorMemory(db.Model):
    __tablename__ = 'monitor_memory'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total = db.Column(db.Integer, nullable=False, comment='总内存')
    free = db.Column(db.Integer, nullable=False, comment='空闲内存')
    buffers = db.Column(db.Integer, nullable=False, comment='缓冲大小')
    cached = db.Column(db.Integer, nullable=False, comment='缓冲存储器')
    swap_cached = db.Column(db.Integer, nullable=False, comment='交换空间缓冲存储器')
    swap_total = db.Column(db.Integer, nullable=False, comment='交换空间总大小')
    swap_free = db.Column(db.Integer, nullable=False, comment='交换空间空闲总大小')
    swap_rate = db.Column(db.String(100), nullable=False, comment='交换空间利用率')
    rate = db.Column(db.Integer, nullable=False, comment='内存利用率')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

db.create_all()
