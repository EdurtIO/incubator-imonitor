#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:45:26
# @Desc    : host数据服务
# @File    : service_host.py

from sqlalchemy import desc

from application_config import db
from db.models import Host, User


class HostService:

    def find_all(self):
        """
        查询所有数据
        :return: 数据集合
        """
        return Host().query.all()

    def find_one(self, id=int):
        return Host().query.filter_by(id = id).first()

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
        except Exception, ex:
            print ex
            return False

    def count(self):
        return Host().query.count()

    def count_by_user(self, user=User):
        return Host().query.filter((Host.users.any(User.id == user.id))).count()

    def update_one(self, host=Host):
        try:
            db.session.query(Host).filter(Host.id == host).update(host)
            db.session.commit()
            return True
        except Exception, ex:
            print ex
            return False