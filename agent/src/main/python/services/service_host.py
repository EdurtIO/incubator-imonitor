#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:45:26
# @Desc    : host数据服务
# @File    : service_host.py

from flask import flash
from sqlalchemy import desc, text

from application_config import db, logger
from db.models import Host, User

logger_type = 'host_service'


class HostService:

    def find_all(self):
        """
        查询所有数据
        :return: 数据集合
        """
        return Host().query.all()

    def find_one(self, id=int):
        return Host().query.filter_by(id=id).first()

    def find_all_order_by_create_time_desc(self):
        return Host().query.order_by(desc(Host.create_time)).all()

    def find_all_order_by_create_time_desc_and_user(self, user=User):
        return Host().query.filter((Host.users.any(User.id == user.id))).order_by(desc(Host.create_time)).all()

    def add(self, host=Host):
        """
        添加数据
        :param host: 主机数据
        :return: 添加状态
        """
        try:
            db.session.add(host)
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def count(self):
        return Host().query.count()

    def count_by_user(self, user=User):
        # sql = 'select count(h.id) from host as h ' \
        #       'left join user_host_relation as uhr on h.id = uhr.host_id ' \
        #       'left join user as u on u.id = uhr.user_id ' \
        #       'where u.id = :id'
        # print(db.engine.execute(
        #     text(sql), {'id': user.id}
        # ))
        # return db.engine.execute(
        #     text(sql), {'id': user.id}
        # )
        return Host().query.filter((Host.users.any(User.id == user.id))).count()

    def update_one(self, host=Host):
        try:
            logger.info('execute update %s starting primary key <%s>', logger_type, host.id)
            sql = 'update `host` set hostname = :hostname, username = :username, password = :password, `key` = :key, ' \
                  'server_name = :server_name, server_type = :server_type, server = :server, command = :command, ' \
                  'command_start = :command_start, command_stop = :command_stop, command_restart = :command_restart,' \
                  'message = :message, ssh_port = :ssh_port where id = :id'
            db.engine.execute(
                text(sql), {'hostname': host.hostname, 'username': host.username, 'password': host.password,
                            'key': host.key, 'server_name': host.server_name,
                            'server_type': host.server_type, 'server': host.server, 'command': host.command,
                            'command_start': host.command_start,
                            'command_stop': host.command_stop, 'command_restart': host.command_restart,
                            'message': host.message, 'ssh_port': host.ssh_port, 'id': host.id}
            )
            logger.info('execute update %s starting primary key <%s> success', logger_type, host.id)
            return True
        except Exception as ex:
            logger.info('execute update %s starting primary key <%s> error, reason <%s>', logger_type, host.id, ex)
            flash('更新数据失败, 错误如下: \r\n{}'.format(ex))
            return False

    def delete_one(self, id=int):
        host = Host().query.filter_by(id=id).first()
        if host is not None:
            db.session.delete(host)
            db.session.commit()
