#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-19 22:17:30
# @File    : service.py
import datetime

from application_config import db
from model.base import BaseModel


class ServiceModel(db.Model, BaseModel):
    __tablename__ = 'service'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='service name')
    compileWay = db.Column('compile_way', db.String(100), nullable=False, comment='compile way')
    gitRemote = db.Column('git_remote', db.String(220), nullable=True, comment='git remote')
    gitUsername = db.Column('git_username', db.String(220), nullable=True, comment='git username')
    gitPassword = db.Column('git_password', db.String(220), nullable=True, comment='git password')
    download = db.Column('download', db.String(220), nullable=True, comment='binary download address')
    sourceRoot = db.Column('source_root', db.String(220), nullable=True, comment='binary download address')
    state = db.Column(db.String(220), nullable=True)
    message = db.Column(db.Text, nullable=True)
    loggerFile = db.Column('logger_file', db.String(220), nullable=True, comment='logger file')
    createTime = db.Column('create_time', db.DateTime, nullable=False, default=datetime.datetime.now,
                           comment='create time')

db.create_all()
