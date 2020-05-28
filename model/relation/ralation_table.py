#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-20 00:20
# @File    : ralation_table.py
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from model.model_host import HostModel
from model.service import ServiceModel

Base = declarative_base()


class ServiceAndRelation(Base):
  __tablename__ = 'service_host_relation'
  service_id = Column(Integer, ForeignKey(ServiceModel.id), primary_key=True)
  host_id = Column(Integer, ForeignKey(HostModel.id), primary_key=True)
  services = relationship(ServiceModel, backref="hosts")
  hosts = relationship(HostModel, backref="services")
