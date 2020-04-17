#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-17 00:03:03
# @Desc    : 设置脚本
# @File    : view_settings.py
from application_config import logger
from db.models import User
from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from form.form_settings import SettingsProfileForm, BuildModelToFrom

from services.service_user import UserService

logger_type = 'user_view'

settings_view = Blueprint('settings_view', __name__, template_folder='templates')


@settings_view.route('/profile', methods=['GET', 'POST'])
@settings_view.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id=int):
    form_profile = SettingsProfileForm()
    user = UserService().find_one(id=current_user.id)
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
                           active_menu='profile', user=user, alert_type=alter_type)
