#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-28 22:41
# @File    : maven.py
import os
import shutil

from application_config import application, logger
from utils.command import CommandUtils
from utils.precondition import Preconditions


class MavenModel:

  def __init__(self, location=None, loggerFile=None):
    Preconditions.check_not_null(property='location', source=location)
    self.location = location
    self.loggerFile = loggerFile


class Maven:

  def __init__(self, model=MavenModel):
    self.model = model

  def copy(self):
    location = os.path.dirname(application.instance_path)
    os.chdir(location)
    mavenWrapper = os.path.join(location, 'vendor', 'maven')
    for f in os.listdir(mavenWrapper):
      CommandUtils.run_command(command='''echo copy file {} >> {}'''.format(f, self.model.loggerFile))
      source = os.path.join(mavenWrapper, f)
      target = self.model.location
      try:
        if os.path.exists(source) and not os.path.exists(os.path.join(target, f)):
          shutil.copy2(src=source, dst=target)
      except Exception as ex:
        logger.error('copy file error %s, retry copy dir', ex)
        if not os.path.exists(source):
          shutil.copytree(src=source, dst=os.path.join(target, f))

  def clone(self):
    os.chdir(self.model.location)
    CommandUtils.run_command_response_to_file(command='./mvnw clean package -DskipTests -X',
                                              loggerFile=self.model.loggerFile)


if __name__ == '__main__':
  model = MavenModel(location='/Users/shicheng/Documents/java-design-patterns',
                     loggerFile='/Users/shicheng/Documents/a.log')
  maven = Maven(model=model)
  maven.copy()
  maven.clone()
