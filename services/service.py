#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : service_command_execute.py

from application_config import db, logger
from model.model_service import ServiceModel

import traceback

logger_type = 'service'


class Service:

    def find_all(self):
        return ServiceModel().query.all()

    def find_one(self, id=int):
        return ServiceModel().query.filter_by(id=id).first()

    def save(self, model=ServiceModel, user_id=None):
        try:
            logger.info('execute update %s starting primary key <%s>', logger_type, user_id)
            db.session.add(model)
            db.session.commit()
            logger.info('execute update %s starting primary key <%s> success', logger_type, user_id)
            return True
        except Exception as ex:
            traceback.print_exc()
            logger.error('execute update %s starting primary key <%s> error, reason <%s>', logger_type, user_id, ex)
            return False
