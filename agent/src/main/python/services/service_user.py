#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:45:26
# @Desc    : host数据服务
# @File    : service_host.py

import datetime
from application_config import db, logger
from db.models import User
from flask import flash
from sqlalchemy import text

logger_type = 'user'


class UserService:

    def find_by_email(self, email):
        return User().query.filter_by(email=email).first()

    def find_one(self, id=int):
        return User().query.filter_by(id=id).first()

    def add(self, user=User):
        try:
            user.set_password(user.password)
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def update_one(self, user=User):
        try:
            logger.info('execute update %s starting primary key <%s>', logger_type, user.id)
            sql = 'update user set name = :name, email = :email, position = :position, description = :description, ' \
                  'website = :website where id = :id'
            db.engine.execute(
                text(sql),
                {'name': user.name, 'email': user.email, 'position': user.position, 'description': user.description,
                 'website': user.website, 'id': user.id}
            )
            logger.info('execute update %s starting primary key <%s> success', logger_type, user.id)
            return True
        except Exception as ex:
            logger.info('execute update %s starting primary key <%s> error, reason <%s>', logger_type, user.id, ex)
            flash('更新数据失败, 错误如下: \r\n{}'.format(ex))
            return False

    def update_password(self, user=User):
        try:
            logger.info('execute update %s starting primary key <%s>', logger_type, user.id)
            user.set_password(user.password)
            sql = 'update user set password = :password where id = :id'
            db.engine.execute(
                text(sql),
                {'password': user.password, 'id': user.id}
            )
            logger.info('execute update %s starting primary key <%s> success', logger_type, user.id)
            return True
        except Exception as ex:
            logger.info('execute update %s starting primary key <%s> error, reason <%s>', logger_type, user.id, ex)
            flash('更新数据失败, 错误如下: \r\n{}'.format(ex))
            return False

    def update_last_login_time(self, user=User):
        try:
            logger.info('execute update %s starting primary key <%s>', logger_type, user.id)
            user.last_login_time = datetime.datetime.now()
            sql = 'update user set last_login_time = :last_login_time where id = :id'
            db.engine.execute(
                text(sql),
                {'last_login_time': user.last_login_time, 'id': user.id}
            )
            logger.info('execute update %s starting primary key <%s> success', logger_type, user.id)
            return True
        except Exception as ex:
            logger.info('execute update %s starting primary key <%s> error, reason <%s>', logger_type, user.id, ex)
            return False
