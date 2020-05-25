#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-08 16:40:20
# @Desc    : 授权配置
# @File    : user.py
import re

from flask import Blueprint, flash, redirect, render_template, url_for
from flask import request
from flask_login import current_user, login_user, logout_user

from application_config import application, logger
from application_config import login_manager
from bin.assets import compile_auth_assets
from db.model_logging_login import LoginLogging
from db.models import User
from form.user import FormSignIn, FormSignUp
from services.service_logging_login import LoginLoggingService
from services.service_user import UserService

UserView = Blueprint('UserView', __name__, template_folder='templates', static_folder='static')

compile_auth_assets(application)


@UserView.route('/signin', methods=['GET', 'POST'])
def signin():
    logging_login = LoginLogging()
    logging_login.ip = request.remote_addr
    if current_user.is_authenticated:
        logging_login.status = True
        logging_login.reason = 'The current user is logged in!'
        LoginLoggingService().add(model=logging_login, user_id=current_user.id)
        return redirect(url_for('dashboard_view.index'))
    login_form = FormSignIn()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            name = login_form.name.data
            password = login_form.password.data
            login_type = re.match(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', name)
            if login_type is None:
                user = UserService().find_by_username(name=name)
            else:
                user = UserService().find_by_email(email=name)
            if user and user.check_password(password=password):
                login_user(user)
                UserService().update_last_login_time(user)
                next_page = request.args.get('next')
                logging_login.status = True
                LoginLoggingService().add(model=logging_login, user_id=current_user.id)
                return redirect(next_page or url_for('dashboard_view.index'))
            else:
                logging_login.status = False
                logging_login.reason = 'Incorrect password entered!'
                # Anonymous user login does not do storage
                try:
                    LoginLoggingService().add(model=logging_login, user_id=user.id)
                    flash('Incorrect password entered!')
                except Exception as ex:
                    flash('Invalid account information!')
                    logger.error('not found <%s> user', login_form.name.data)
                return redirect(url_for('UserView.signin'))
    return render_template('auth/signin.html', form=login_form, title='User SignIn')


@UserView.route('/sign_out')
def logout():
    logout_user()
    flash(u'The current user has logged out!')
    return redirect(url_for('UserView.signin'))


@UserView.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = FormSignUp()
    if request.method == 'POST':
        if signup_form.validate_on_submit():
            name = signup_form.name.data
            email = signup_form.email.data
            password = signup_form.password.data
            confirm_password = signup_form.confirm_password.data
            existing_user = UserService().find_by_email(email=email)
            if existing_user is None:
                user = User(name=name, email=email, password=password)
                if UserService().add(user=user):
                    login_user(user)
                    return redirect(url_for('dashboard_view.index'), code=400)
            flash('The email address has been registered!')
            return redirect(url_for('UserView.signup'))
    return render_template('auth/signup.html', title='User SignUp', form=signup_form)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You do not have access to the current page, please log in.')
    return redirect(url_for('UserView.signin'))
