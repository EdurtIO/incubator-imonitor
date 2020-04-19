#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : service_command_execute.py

from application_config import db, logger
from db.model_host import HostConnection
from sqlalchemy import desc, text

logger_type = 'host_connection_service'


class HostConnectionService:

    def find_all(self):
        return HostConnection().query.all()

    def find_one(self, id=int):
        return HostConnection().query.filter_by(id=id).first()

    def find_all_order_by_create_time_desc(self):
        return HostConnection().query.order_by(desc(HostConnection.create_time)).all()

    def find_all_by_host_create_time_desc(self, host_id=int):
        try:
            logger.info('execute select %s starting primary key <%s>', logger_type, host_id)
            sql = 'select hc.name, hc.type, hc.start_time, hc.end_time, hc.elapsed_time, hc.reason, h.hostname, h.username ' \
                  'from host_connection as hc ' \
                  'left join user_host_connection as uhc on hc.id = uhc.connection_id ' \
                  'left join user as u on uhc.user_id = u.id ' \
                  'left join host as h on uhc.host_id = h.id ' \
                  'where h.id = :host_id ' \
                  'order by hc.create_time desc '
            result = db.engine.execute(
                text(sql), {'host_id': host_id}
            )
            return [dict(row) for row in result]
        except Exception as ex:
            logger.info('execute select %s starting primary key <%s> error, reason <%s>', logger_type, host_id, ex)
            return None

    def add(self, model=HostConnection, user_id=int, host_id=int):
        try:
            logger.info('execute update %s starting primary key <%s>', logger_type, user_id)
            db.session.add(model)
            db.session.commit()
            sql = 'insert into user_host_connection(host_id, user_id, connection_id) ' \
                  'values(:host_id, :user_id, :connection_id)'
            db.engine.execute(
                text(sql), {'host_id': host_id, 'user_id': user_id, 'connection_id': model.id}
            )
            logger.info('execute update %s starting primary key <%s> success', logger_type, user_id)
            return True
        except Exception as ex:
            logger.info('execute update %s starting primary key <%s> error, reason <%s>', logger_type, user_id, ex)
            return False
