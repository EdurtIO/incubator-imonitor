#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-14 22:41
# @File    : service.py
import os

from flask import Blueprint, flash, redirect, render_template, request, url_for, make_response
from flask_login import login_required

from common.state import State
from form.service import BuildModelToFrom, ServiceForm
from model.service import ServiceModel
from services.service import Service
from utils.git import Git, GitModel

ServiceView = Blueprint('ServiceView', __name__, template_folder='templates')

logger_type = 'ServiceView'


@ServiceView.route('/list', methods=['GET'])
@login_required
def index():
  models = Service().find_all()
  return render_template('service/list.html', active_menu='service', models=models)


@ServiceView.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  form = ServiceForm()
  if form.validate_on_submit():
    model = ServiceModel()
    model.name = request.form.get('name')
    model.compileWay = request.form.get('compileWay')
    model.state = State.INITED.name
    if model.compileWay is '0':
      model.gitRemote = request.form.get('gitRemote')
      model.gitUsername = request.form.get('gitUsername')
      model.gitPassword = request.form.get('gitPassword')
    else:
      model.gitRemote = None
      model.gitUsername = None
      model.gitPassword = None
      model.download = request.form.get('binary')
    model.sourceRoot = request.form.get('sourceRoot')
    if Service().save(model=model):
      flash('''Create <{}> Service Success!'''.format(model.name))
      return redirect(url_for('ServiceView.index'))
  return render_template('service/create.html', form=form, active_menu='service', title='Create new Service')


@ServiceView.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def home(id=int):
  model = Service().find_one(id=id)
  form = ServiceForm()
  BuildModelToFrom(model=model, form=form)
  if form.validate_on_submit():
    model = ServiceModel()
    model.id = id
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
      model.download = request.form.get('download')
    model.sourceRoot = request.form.get('sourceRoot')
    if Service().update(model=model):
      flash('''Update <{}> Service Success!'''.format(model.name))
      return redirect(url_for('ServiceView.index'))
  return render_template('service/index.html', active_menu='service', form=form)


@ServiceView.route('reload/<int:id>', methods=['GET'])
@login_required
def reload(id=int):
  model = Service().find_one(id=id)
  if model.compileWay is '0':
    loggerFile = os.path.join(model.sourceRoot, '''{}.log'''.format(model.name))
    model.loggerFile = loggerFile
    Service().update(model=model)
    gitModel = GitModel(url=model.gitRemote, username=model.gitUsername, password=model.gitPassword,
                        target=os.path.join(model.sourceRoot, model.name), loggerFile=loggerFile, id=model.id)
    git = Git(model=gitModel)
    git.clone()
  else:
    pass
  return redirect(url_for('ServiceView.index'))


@ServiceView.route('logger/<int:id>', methods=['GET'])
@login_required
def logger(id=int):
  model = Service().find_one(id=id)
  if model.loggerFile:
    response = make_response(open(model.loggerFile).read())
    response.headers["Content-type"]="text/plan;charset=UTF-8"
    return response
  else:
    flash('Not Found Logger!')
  return redirect(url_for('ServiceView.index'))

