#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 19:05:18
# @Desc    : MySQL客户端脚本
# @File    : MySql.py

from flaskext.mysql import MySQL

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'test'
mysql = MySQL()
mysql.init_app(app)


class MySqlClient:

    def get_client(self):
        """
        获取mysql数据库连接指针
        :return: 数据库指针
        """
        try:
            return mysql.get_db().cursor()
        except Exception:
            return None

    def insert(self, sql):
        if sql is not None:
            cursor = self.get_client()
        else:
            print 1
