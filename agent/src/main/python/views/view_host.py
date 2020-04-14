#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 23:25:25
# @Desc    : 主机视图脚本
# @File    : view_host.py

from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user
from flask_login import login_required

from common.utils import CommandUtils
from db.models import Host
from form.form_host import host_create_form
from services.service_host import HostService

host_view = Blueprint('host_view', __name__, template_folder='templates')


@host_view.route('/', methods=['GET'])
@host_view.route('/list', methods=['GET'])
@login_required
def list():
    return render_template('host/host-list.html',
                           hosts=HostService().find_all_order_by_create_time_desc_and_user(current_user))


@host_view.route('/cmcd/', defaults={'host_id': 0}, methods=['GET', 'POST', 'PUT'])
@host_view.route('/cmcd/<int:host_id>', methods=['GET', 'POST', 'PUT'])
@login_required
def create_modfiy_copy_delete(host_id=int):
    type = request.args.get('type')
    method = request.args.get('method')
    form = host_create_form()
    host = HostService().find_one(id=host_id)
    if (host_id <= 0) or host is None:
        title = '新建主机'
    else:
        # # 重新渲染表单支持select标签回显数据
        form.server.default = host.server
        # form.process(form)
        if (host_id > 0 and type is None):
            title = '修改主机'
        else:
            title = '复制主机'
    if form.validate_on_submit():
        host = Host()
        host.hostname = form.hostname.data
        host.active = True
        host.username = form.username.data
        host.password = form.password.data
        host.command = form.command.data
        host.command_start = form.command_start.data
        host.command_stop = form.command_stop.data
        host.command_restart = form.command_restart.data
        host.server_name = form.server_name.data
        host.server_type = form.server_type.data
        host.server = form.server.data
        host.users = [current_user]
        if form.submit.data:
            if method == 'PUT':
                host.id = form.id.data
                if HostService().update_one(host):
                    return redirect('/host')
            elif request.method == 'POST':
                if HostService().add(host):
                    return redirect('/host')
        if form.test_connection.data:
            buffer = CommandUtils().command_ssh_remote(form.username, form.hostname, form.password, form.command)
            flash('用户 <{}> 连接主机 <{}> 失败，错误如下\n：{}'.format(form.hostname.data, form.username.data,
                  buffer.before))
            return redirect(url_for('host_view.create_modfiy_copy_delete'))
    return render_template('host/host.html', form=form, host=host, title=title)


@host_view.route('/delete/<int:host_id>', methods=['GET'])
@login_required
def delete(host_id=int):
    HostService().delete_one(host_id)
    return redirect(url_for('host_view.list'))
