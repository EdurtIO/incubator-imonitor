#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 23:25:25
# @Desc    : 主机视图脚本
# @File    : view_host.py

from common.ssh import Ssh
from common.utils import StringUtils
from db.models import Host
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user
from flask_login import login_required
from form.form_host import HostForm, BuildModelToFrom
from services.service_host import HostService
from application_config import logger

host_view = Blueprint('host_view', __name__, template_folder='templates')

logger_type = 'host_view'

@host_view.route('/', methods=['GET'])
@host_view.route('/list', methods=['GET'])
@login_required
def index():
    return render_template('host/host-list.html',
                           hosts=HostService().find_all_order_by_create_time_desc_and_user(current_user),
                           active_menu='host')


@host_view.route('/cmcd/', defaults={'host_id': 0}, methods=['GET', 'POST', 'PUT'])
@host_view.route('/cmcd/<int:host_id>', methods=['GET', 'POST', 'PUT'])
@login_required
def create_modfiy_copy_delete(host_id=int):
    type = request.args.get('type')
    method = request.args.get('method')
    form = HostForm()
    host = HostService().find_one(id=host_id)
    if (host_id <= 0) or host is None:
        title = '新建主机'
    else:
        # 回显表单数据
        BuildModelToFrom(host=host, form=form)
        if (host_id > 0 and type is None):
            title = '修改主机'
        else:
            title = '复制主机'
    if form.validate_on_submit():
        host = Host()
        host.hostname = request.form.get('hostname')
        host.active = True
        host.username = request.form.get('username')
        host.password = request.form.get('security_password')
        host.command = request.form.get('command')
        host.command_start = request.form.get('command_start')
        host.command_stop = request.form.get('command_stop')
        host.command_restart = request.form.get('command_restart')
        host.server_name = request.form.get('server_name')
        host.server_type = request.form.get('server_type')
        host.server = request.form.get('server')
        host.users = [current_user]
        host.ssh_port = request.form.get('ssh_port')
        host.key = form.security_key.data
        if form.submit.data:
            if method == 'PUT':
                host.id = host_id
                if request.form.get('security') == '1':
                    host.key = None
                else:
                    host.password = None
                logger.info('execute update operation type <%s> primary key <%s>', logger_type, host_id)
                if HostService().update_one(host):
                    return redirect(url_for('host_view.index'))
            elif request.method == 'POST':
                if HostService().add(host):
                    return redirect(url_for('host_view.index'))
        if form.test_connection.data:
            ssh_connect = Ssh(hostname=host.hostname, port=host.ssh_port, username=host.username,
                              password=host.password,
                              private_key=host.key)
            if ssh_connect.check_connect() is False:
                flash('用户 <{}> 连接主机 <{}> 失败，错误如下：\r\n{}'.format(host.hostname, host.username, ssh_connect.get_message()))
            else:
                flash('用户 <{}> 连接主机 <{}> 成功！'.format(host.hostname, host.username))
                if StringUtils().is_not_empty(method):
                    return redirect(url_for('host_view.create_modfiy_copy_delete', host_id=host_id, method=method))
                else:
                    return redirect(url_for('host_view.create_modfiy_copy_delete', host_id=host_id))
    return render_template('host/host.html', form=form, host=host, title=title, active_menu='host')


@host_view.route('/delete/<int:host_id>', methods=['GET'])
@login_required
def delete(host_id=int):
    HostService().delete_one(host_id)
    return redirect(url_for('host_view.index', active_menu='host'))
