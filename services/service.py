#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : service_command_execute.py
import traceback

from flask_login import current_user

from application_config import db, logger
from model.service import ServiceModel

loggerType = 'service'


class Service:

    def __init__(self):
        self.userId = current_user.id

    def find_all(self):
        return ServiceModel().query.all()

    def find_one(self, id=int):
        return ServiceModel().query.filter_by(id=id).first()

    def save(self, model=ServiceModel):
        try:
            logger.info('execute %s starting primary key <%s>', loggerType, self.userId)
            db.session.add(model)
            db.session.commit()
            logger.info('execute %s starting primary key <%s> success', loggerType, self.userId)
            return True
        except Exception as ex:
            traceback.print_exc()
            logger.error('execute %s starting primary key <%s> error, reason <%s>', loggerType, self.userId, ex)
            return False
