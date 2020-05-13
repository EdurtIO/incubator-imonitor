#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-13 18:27:03
# @Desc    : Web Terminal脚本
# @File    : view_terminal.py
from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user
from flask_login import login_required
from services.service_host import HostService

terminal_view = Blueprint('terminal_view', __name__, template_folder='templates')


@terminal_view.route('/open/<int:host_id>', methods=['GET'])
@login_required
def index(host_id=int):
    host = HostService().find_one(host_id)
    if host_id is None or host is None:
        return redirect(url_for('host_view.list'))
    count = HostService().count_by_user()
    return render_template('terminal/terminal.html', title='{}-终端'.format(host.hostname), server_id=host_id,
                           user=current_user)
