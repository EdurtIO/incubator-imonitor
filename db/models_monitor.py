#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:09:04
# @Desc    : 实体类
# @File    : models_monitor.py
import datetime
from application_config import db
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import class_mapper


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
    rate = db.Column(DOUBLE(10, 4), nullable=False, comment='内存利用率')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)


class MonitorCpu(db.Model):
    __tablename__ = 'monitor_cpu'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpu_time_1 = db.Column(db.BigInteger, nullable=False, comment='总CPU时间1')
    cpu_time_2 = db.Column(db.BigInteger, nullable=False, comment='总CPU时间2')
    idle = db.Column(db.String(20), nullable=False, comment='计算空闲时间')
    rate = db.Column(DOUBLE(10, 4), nullable=False, comment='利用率')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)


class MonitorNetworkIO(db.Model):

    __tablename__ = 'monitor_network_io'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='网卡名称')
    receive = db.Column(DOUBLE(10, 4), nullable=False, comment='接受速度(单位KB/s)')
    transmit = db.Column(DOUBLE(10, 4), nullable=False, comment='发送速度(单位KB/s)')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def as_dict(obj):
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # 上面的有缺陷，表字段和属性不一致会有问题
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c)


db.create_all()
