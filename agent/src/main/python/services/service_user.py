#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:45:26
# @Desc    : host数据服务
# @File    : service_host.py

from application_config import db
from db.models import User


class UserService:

    def find_by_email(self, email):
        return User().query.filter_by(email=email).first()

    def add(self, user=User):
        try:
            user.set_password(user.password)
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False
