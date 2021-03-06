#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-17 00:03:03
# @Desc    : 用户设置脚本
# @File    : view_settings.py
import os
import time
from application_config import logger, codes
from db.models import User
from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from form.form_settings import SettingsProfileForm, BuildModelToFrom, SettingsSecurityForm, SettingsAvatarForm
from services.service_logging_login import LoginLoggingService
from services.service_user import UserService

logger_type = 'settings_view'

settings_view = Blueprint('settings_view', __name__, template_folder='templates')


@settings_view.route('/profile', methods=['GET', 'POST'])
@settings_view.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id=int):
    form_profile = SettingsProfileForm()
    form_avatar = SettingsAvatarForm()
    user = UserService().find_one(id=current_user.id)
    if form_avatar.validate_on_submit():
        avatar = request.files['avatar']
        path = '{}/{}'.format(codes['config']['avatar'], current_user.id)
        if not os.path.exists(path):
            os.makedirs(path)
        avatar_path = os.path.join(codes['config']['avatar'], '{}/{}.png'.format(current_user.id, int(time.time())))
        avatar.save(avatar_path)
        user.avatar = '{}/{}.png'.format(current_user.id, int(time.time()))
        if UserService().update_avatar(user=user):
            flash('数据更新成功！')
        return redirect(url_for('settings_view.profile', alert_type='success'))
    BuildModelToFrom(user, form_profile)
    if form_profile.validate_on_submit():
        user = User()
        user.id = current_user.id
        user.name = request.form.get('username')
        user.website = request.form.get('website')
        user.position = request.form.get('position')
        user.description = request.form.get('description')
        user.email = request.form.get('email')
        if request.method == 'POST':
            logger.info('execute update operation type <%s> primary key <%s>', logger_type, user.id)
            if UserService().update_one(user=user):
                flash('数据更新成功！')
                return redirect(url_for('settings_view.profile', alert_type='success'))
    if request.args.get('alert_type') is None:
        alter_type = 'danger'
    else:
        alter_type = request.args.get('alert_type')
    return render_template('settings/settings-profile.html', user_id=user_id, title='个人资料', form_profile=form_profile,
                           active_menu='profile', user=user, alert_type=alter_type, avatar_form=form_avatar)

@settings_view.route('/security', methods=['GET', 'POST'])
@login_required
def security():
    form = SettingsSecurityForm()
    if form.validate_on_submit():
        old_password = request.form.get('old_password')
        password = request.form.get('password')
        if current_user.check_password(old_password):
            current_user.password = password
            if UserService().update_password(user=current_user):
                flash('密码更新成功！')
                return redirect(url_for('settings_view.security', alert_type='success'))
        else:
            flash('原密码输入错误')
            return redirect(url_for('settings_view.security'))
    if request.args.get('alert_type') is None:
        alter_type = 'danger'
    else:
        alter_type = request.args.get('alert_type')
    return render_template('settings/settings-security.html', title='安全设置', active_menu='security', form=form,
                           alert_type=alter_type)


@settings_view.route('/logging_login', methods=['GET'])
@login_required
def logging_login():
    loggings = LoginLoggingService().find_all_order_by_user_and_login_time_desc(current_user.id)
    return render_template('settings/settings-logging-login.html', title='登录日志', active_menu='logging-login',
                           loggings=loggings)
