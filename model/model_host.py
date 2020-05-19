#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-20 00:34
# @File    : model_host.py
import datetime

from application_config import db
from model.model_base import BaseModel


class HostModel(db.Model, BaseModel):
  __tablename__ = 'hosts'
  __table_args__ = {"extend_existing": True}
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  hostname = db.Column(db.String(100), nullable=False)
  port = db.Column(db.Integer, nullable=False)
  username = db.Column(db.String(100), nullable=False)
  password = db.Column(db.String(100), nullable=True)
  key = db.Column(db.Text, nullable=True)
  active = db.Column(db.Boolean, nullable=False, default=True)
  create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
