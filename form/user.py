#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-08 15:54:15
# @File    : from_auth.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class FormSignIn(FlaskForm):
  name = StringField('User', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('SignIn')


class FormSignUp(FlaskForm):
  name = StringField('UserName',
                     validators=[Length(min=6, message='Please enter a valid password of at least 6 digits'),
                                 DataRequired()])
  email = StringField('Email',
                      validators=[Length(min=6, message='Please enter a valid password of at least 6 digits')])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6,
                                                                          message='Please enter a valid password of at least 6 digits')])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                           message='The passwords entered do not match')])
  submit = SubmitField('SignUp')
