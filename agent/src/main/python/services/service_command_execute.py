#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : service_command_execute.py

from application_config import db, logger
from db.model_command_execute import CommandExecute
from sqlalchemy import desc, text

logger_type = 'command_execute_service'


class CommandExecuteService:

    def find_all(self):
        return CommandExecute().query.all()

    def find_one(self, id=int):
        return CommandExecute().query.filter_by(id=id).first()

    def find_all_order_by_create_time_desc(self):
        return CommandExecute().query.order_by(desc(CommandExecute.create_time)).all()

    def find_all_by_host_create_time_desc(self, host_id=int):
        try:
            logger.info('execute select %s starting primary key <%s>', logger_type, host_id)
            sql = 'select ce.command, ce.final_state, ce.start_time, ce.end_time, ce.elapsed_time, ce.reason, h.hostname, u.name ' \
                  'from command_execute as ce ' \
                  'left join user_host_command_execute_relation as uhcer on ce.id = uhcer.command_execute_id ' \
                  'left join user as u on uhcer.user_id = u.id ' \
                  'left join host as h on uhcer.host_id = h.id ' \
                  'where h.id = :host_id ' \
                  'order by ce.create_time desc '
            result = db.engine.execute(
                text(sql), {'host_id': host_id}
            )
            return [dict(row) for row in result]
        except Exception as ex:
            logger.info('execute select %s starting primary key <%s> error, reason <%s>', logger_type, host_id, ex)
            return None

    def add(self, model=CommandExecute, user_id=int, host_id=int):
        try:
            logger.info('execute update %s starting primary key <%s>', logger_type, user_id)
            db.session.add(model)
            db.session.commit()
            sql = 'insert into user_host_command_execute_relation(host_id, user_id, command_execute_id) ' \
                  'values(:host_id, :user_id, :command_execute_id)'
            db.engine.execute(
                text(sql), {'host_id': host_id, 'user_id': user_id, 'command_execute_id': model.id}
            )
            logger.info('execute update %s starting primary key <%s> success', logger_type, user_id)
            return True
        except Exception as ex:
            logger.info('execute update %s starting primary key <%s> error, reason <%s>', logger_type, user_id, ex)
            return False

    def count(self):
        return CommandExecute().query.count()
