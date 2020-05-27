#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-16 22:56
# @File    : form_service.py
from flask_wtf import FlaskForm
from wtforms import PasswordField, RadioField, StringField, SubmitField
from wtforms.validators import DataRequired


class ServiceCreateForm(FlaskForm):
  name = StringField(u'Service Name',
                     validators=[DataRequired(message=u'service name must not null')],
                     render_kw={'placeholder': 'please input service name', 'size': 'mini'})
  compileWay = RadioField(u'Compile Way',
                          choices=[('0', 'Source'), ('1', 'Binary')], default='0', validators=[DataRequired()])
  gitRemote = StringField(u'Git Remote',
                          validators=[DataRequired(message=u'git remote must not null')],
                          render_kw={'placeholder': 'please input git remote address', 'size': 'mini'})
  gitUsername = StringField(u'Git UserName',
                            validators=[DataRequired(message=u'git username must not null')],
                            render_kw={'placeholder': 'please input git username', 'size': 'mini'})
  gitPassword = PasswordField(u'Git Password',
                              validators=[DataRequired(message=u'git password must not null')],
                              render_kw={'placeholder': 'please input git password', 'size': 'mini'})
  download = StringField(u'Download Address',
                         validators=[DataRequired(message=u'download address must not null')],
                         render_kw={'placeholder': 'please input download address', 'size': 'mini'})
  sourceRoot = StringField(u'Source Root Path',
                           validators=[DataRequired(message=u'install root path must not null')],
                           render_kw={'placeholder': 'please input install root path', 'size': 'mini'})
  submit = SubmitField(u'Submit',
                       render_kw={'class': 'btn btn-primary', 'size': 'mini'})
