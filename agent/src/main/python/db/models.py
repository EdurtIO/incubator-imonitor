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
    ssh_port = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=True)
    key = db.Column(db.Text, nullable=True)
    server_name = db.Column(db.String(100), nullable=False)
    server_type = db.Column(db.String(100), nullable=False)
    server = db.Column(db.String(100), nullable=False)
    command = db.Column(db.String(255), nullable=True)
    command_start = db.Column(db.String(255), nullable=True)
    command_stop = db.Column(db.String(255), nullable=True)
    command_restart = db.Column(db.String(255), nullable=True)
    message = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    users = db.relationship('User', secondary='user_host_relation',
                            backref=db.backref('users', lazy='dynamic'), lazy='dynamic',
                            passive_deletes=True)
    # active = db.Column(db.Boolean, nullable=False, server_default=True, comment='激活状态，默认为激活（True）')


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """
    用户模型
    """
    __tablename__ = 'user'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    website = db.Column(db.String(200), primary_key=False, unique=False, nullable=True)
    description = db.Column(db.Text, nullable=True)
    position = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String(200), primary_key=False, unique=False, nullable=True)
    create_time = db.Column(db.DateTime, index=False, unique=False, nullable=True, default=datetime.datetime.now)
    last_login_time = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    hosts = db.relationship('Host', secondary='user_host_relation',
                            backref=db.backref('hosts', lazy='dynamic'), lazy='dynamic',
                            passive_deletes=True)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)


user_host_relation = db.Table('user_host_relation',
                              db.Column('user_id', db.Integer,
                                        db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'),
                                        primary_key=True),
                              db.Column('host_id', db.Integer,
                                        db.ForeignKey('host.id', ondelete='CASCADE', onupdate='CASCADE'),
                                        primary_key=True)
                              )

db.create_all()
