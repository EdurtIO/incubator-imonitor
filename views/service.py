#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-14 22:41
# @File    : service.py
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from form.service import ServiceCreateForm
from model.service import ServiceModel
from services.service import Service

ServiceView = Blueprint('ServiceView', __name__, template_folder='templates')

logger_type = 'ServiceView'


@ServiceView.route('/', methods=['GET'])
@ServiceView.route('/list', methods=['GET'])
@login_required
def index():
  models = Service().find_all()
  return render_template('service/list.html', active_menu='service', models=models)


@ServiceView.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  form = ServiceCreateForm()
  if form.validate_on_submit():
    model = ServiceModel()
    model.name = request.form.get('name')
    model.compileWay = request.form.get('compileWay')
    if model.compileWay is '0':
      model.gitRemote = request.form.get('gitRemote')
      model.gitUsername = request.form.get('gitUsername')
      model.gitPassword = request.form.get('gitPassword')
    else:
      model.gitRemote = None
      model.gitUsername = None
      model.gitPassword = None
      model.binary = request.form.get('binary')
    model.sourceRoot = request.form.get('sourceRoot')
    if Service().save(model=model):
      flash('''Create <{}> Service Success!'''.format(model.name))
      return redirect(url_for('ServiceView.index'))
  return render_template('service/create.html', form=form, active_menu='service', title='Create new Service')
