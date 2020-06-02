#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-16 22:56
# @File    : service.py
from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, StringField, SubmitField
from wtforms.validators import DataRequired

from imforms.widgets.password_field import PasswordField
from model.service import ServiceModel


class ServiceForm(FlaskForm):
  id = HiddenField(u'No')
  name = StringField(u'Service Name',
                     validators=[DataRequired(message=u'service name must not null')],
                     render_kw={'placeholder': 'please input service name', 'size': 'mini'})
  compileWay = RadioField(u'Compile Way',
                          choices=[('0', 'Source'), ('1', 'Binary')], default='0', validators=[DataRequired()])
  gitRemote = StringField(u'Git Remote',
                          render_kw={'placeholder': 'please input git remote address', 'size': 'mini'})
  gitUsername = StringField(u'Git UserName',
                            render_kw={'placeholder': 'please input git username', 'size': 'mini'})
  gitPassword = PasswordField(u'Git Password',
                              render_kw={'placeholder': 'please input git password', 'size': 'mini'})
  download = StringField(u'Download Address',
                         render_kw={'placeholder': 'please input download address', 'size': 'mini'})
  sourceRoot = StringField(u'Source Root Path',
                           validators=[DataRequired(message=u'install root path must not null')],
                           render_kw={'placeholder': 'please input install root path', 'size': 'mini'})
  submit = SubmitField(u'Submit',
                       render_kw={'class': 'btn btn-primary', 'size': 'mini'})


class BuildModelToFrom:

  def __init__(self, model=ServiceModel, form=ServiceForm):
    form.id.data = model.id
    form.name.data = model.name
    form.compileWay.data = model.compileWay
    if model.compileWay is '0':
      form.gitRemote.data = model.gitRemote
      form.gitUsername.data = model.gitUsername
      form.gitPassword.data = model.gitPassword
    else:
      form.download.data = model.download
    form.sourceRoot.data = model.sourceRoot
