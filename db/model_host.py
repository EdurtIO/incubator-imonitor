#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from sqlalchemy.orm import class_mapper

from application_config import db


class HostConnection(db.Model):
    __tablename__ = 'host_connection'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='连接会话名称')
    type = db.Column(db.String(100), nullable=True, comment='连接方式')
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='执行开始时间')
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='执行结束时间')
    elapsed_time = db.Column(db.BigInteger, nullable=False, default=0, comment='连接时长')
    reason = db.Column(db.String(100), nullable=True, comment='失败原因')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='数据创建时间')

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c)

db.create_all()
