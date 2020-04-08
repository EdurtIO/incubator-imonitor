#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-08 16:40:20
# @Desc    : 授权配置
# @File    : view_auth.py
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_user, current_user

from application_config import db, app
from application_config import login_manager
from bin.assets import compile_auth_assets
from db.models import User
from form.form_auth import AuthSignin

auth_view = Blueprint('auth_view', __name__, template_folder='templates', static_folder='static')

compile_auth_assets(app)

@auth_view.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    登录视图
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))

    login_form = AuthSignin()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.get('email')
            password = login_form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password=password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main_view.dashboard'))
        flash('无效的账号/密码')
        return redirect(url_for('auth_view.signin'))
    return render_template('auth/signin.html', form=login_form, title='用户登录')


@login_manager.user_loader
def load_user(user_id):
    """
    检查用户是否登录
    :param user_id: 用户ID
    :return: 登录状态
    """
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """
    将未经授权的用户重定向到503界面
    :return: 重定向
    """
    flash('您没有权限访问当前页面，请登录。')
    return redirect(url_for('auth_view.signin'))
