#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-19 22:17:30
# @File    : model_service.py
import datetime

from application_config import db
from model.model_base import BaseModel


class ServiceModel(db.Model, BaseModel):
    __tablename__ = 'service'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='service name')
    compile_way = db.Column(db.String(100), nullable=False, comment='compile way')
    compile_git = db.Column(db.String(220), nullable=True, comment='git remote')
    compile_git_username = db.Column(db.String(220), nullable=True, comment='git username')
    compile_git_password = db.Column(db.String(220), nullable=True, comment='git password')
    binary = db.Column(db.String(220), nullable=True, comment='binary download address')
    install = db.Column(db.String(220), nullable=True, comment='binary download address')
    install_username = db.Column(db.String(220), nullable=True, comment='binary download address')
    install_password = db.Column(db.String(220), nullable=True, comment='binary download address')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='create time')

db.create_all()
