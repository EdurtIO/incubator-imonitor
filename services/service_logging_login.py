#!/usr/bin/env python
# -*- coding: utf-8 -*-

from application_config import db, logger
from db.model_logging_login import LoginLogging
from sqlalchemy import desc, text

logger_type = 'login-logging'


class LoginLoggingService:

    def find_all(self):
        return LoginLogging().query.all()

    def find_one(self, id=int):
        return LoginLogging().query.filter_by(id=id).first()

    def find_all_order_by_create_time_desc(self):
        return LoginLogging().query.order_by(desc(LoginLogging.create_time)).all()

    def add(self, model=LoginLogging, user_id=int):
        try:
            logger.info('execute update %s starting primary key <%s>', logger_type, user_id)
            db.session.add(model)
            db.session.flush()
            db.session.commit()
            sql = 'insert into user_logging_login_relation(user_id, logging_login_id) ' \
                  'values(:user_id, :logging_login_id)'
            db.engine.execute(
                text(sql), {'user_id': user_id, 'logging_login_id': model.id}
            )
            logger.info('execute update %s starting primary key <%s> success', logger_type, user_id)
            return True
        except Exception as ex:
            logger.info('execute update %s starting primary key <%s> error, reason <%s>', logger_type, user_id, ex)
            return False

    def find_all_order_by_user_and_login_time_desc(self, user_id=int):
        try:
            logger.info('execute select %s starting primary key <%s>', logger_type, user_id)
            sql = 'select ll.id as id, ll.login_time as login_time, ll.position as position, ll.ip as ip, ' \
                  'll.client as client, ll.status as status, ll.reason as reason, u.name as username from logging_login as ll ' \
                  'left join user_logging_login_relation as ullr on ll.id = ullr.logging_login_id ' \
                  'left join user as u on u.id = ullr.user_id ' \
                  'where u.id = :user_id ' \
                  'order by ll.login_time desc '
            result = db.engine.execute(
                text(sql), {'user_id': user_id}
            )
            return [dict(row) for row in result]
        except Exception as ex:
            logger.info('execute select %s starting primary key <%s> error, reason <%s>', logger_type, user_id, ex)
            return None
