#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-14 22:41
# @File    : service.py
from flask import Blueprint, render_template
from flask_login import login_required

from form.form_service import ServiceCreateForm

ServiceView = Blueprint('ServiceView', __name__, template_folder='templates')

logger_type = 'ServiceView'


@ServiceView.route('/', methods=['GET'])
@ServiceView.route('/list', methods=['GET'])
@login_required
def index():
  return render_template('service/list.html', active_menu='service')


@ServiceView.route('/', methods=['GET'])
@ServiceView.route('/create', methods=['GET'])
@login_required
def create():
  form = ServiceCreateForm()
  return render_template('service/create.html', form=form, active_menu='service', title='Create new Service')
