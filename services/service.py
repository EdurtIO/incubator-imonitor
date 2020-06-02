#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : service_command_execute.py
import traceback

from flask_login import current_user
from sqlalchemy import text

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

    def update(self, model=ServiceModel):
        try:
            logger.info('execute %s starting primary key <%s>', loggerType, self.userId)
            sql = 'update `service` set '
            if model.name:
                sql += 'name = :name '
            if model.sourceRoot:
                sql += ', source_root = :sourceRoot'
            if model.download:
                sql += ', download = :download'
            if model.gitRemote:
                sql += ', git_remote = :gitRemote'
            if model.gitUsername:
                sql += ', git_username = :gitUsername'
            if model.gitPassword:
                sql += ', git_password = :gitPassword'
            if model.compileWay:
                sql += ', compile_way = :compileWay '
            sql += 'where id = :id'
            db.engine.execute(
                text(sql), {'name': model.name, 'sourceRoot': model.sourceRoot, 'download': model.download,
                            'gitRemote': model.gitRemote, 'gitUsername': model.gitUsername,
                            'gitPassword': model.gitPassword, 'compileWay': model.compileWay, 'id': model.id}
            )
            db.session.commit()
            logger.info('execute %s starting primary key <%s> success', loggerType, self.userId)
            return True
        except Exception as ex:
            traceback.print_exc()
            logger.error('execute %s starting primary key <%s> error, reason <%s>', loggerType, self.userId, ex)
            return False
