#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 14:25:25
# @Desc    : web程序入口脚本
# @File    : Application.py
import json
import sys
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required

from ImonitorService import MonitorService
from controller.Host import HostController
from push import FaIconPush

reload(sys)
sys.setdefaultencoding('utf-8')

from flask_apscheduler import APScheduler

app = Flask(__name__)


class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'monitor_service_heartbeat',
            'func': '__main__:monitor_service_heartbeat',
            # 'args': (1, 2),
            'trigger': 'interval',
            'seconds': 60,
            'max_instances': 1
        }
    ]


app.config.from_object(SchedulerConfig())

import datetime


def monitor_service_heartbeat():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print 'push time {}, push response {}'.format(now,
                                                  FaIconPush.FaIcon().push(json.dumps(MonitorService().service_info())))


app.config['SECRET_KEY'] = 'haha'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/test'  # 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 设置这一项是每次请求结束后都会自动提交数据库中的变动

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required(message=u'密码不能为空')])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           heartbeats=MonitorService().service_info())


@app.route('/host', methods=['GET'])
def host():
    return HostController().hostAddForm()


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
