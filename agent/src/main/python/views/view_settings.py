#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-17 00:03:03
# @Desc    : 设置脚本
# @File    : view_settings.py
from flask import render_template, Blueprint
from flask_login import login_required

from form.form_settings import SettingsProfileForm

settings_view = Blueprint('settings_view', __name__, template_folder='templates')


@settings_view.route('/', methods=['GET'])
@settings_view.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id=int):
    form_profile = SettingsProfileForm()
    return render_template('settings/settings-profile.html', host_id=user_id, title='个人资料', form_profile=form_profile,
                           active_menu='profile')
