#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:45:26
# @Desc    : host数据服务
# @File    : service_host.py

from sqlalchemy import desc, text

from application_config import db
from db.models_monitor import MonitorCpu


class MonitorCpuService:

    def find_all(self):
        return MonitorCpu().query.all()

    def find_one(self, id=int):
        return MonitorCpu().query.filter_by(id=id).first()

    def find_all_order_by_create_time_desc(self):
        return MonitorCpu().query.order_by(desc(MonitorCpu.create_time)).all()

    def add(self, monitor_cpu=MonitorCpu, host_id=int):
        try:
            db.session.add(monitor_cpu)
            db.session.flush()
            db.session.commit()
            sql = 'insert into monitor_cpu_host_relation(host_id, monitor_cpu_id) ' \
                  'values(:host_id, :monitor_cpu_id)'
            db.engine.execute(
                text(sql), {'host_id': host_id, 'monitor_cpu_id': monitor_cpu.id}
            )
            return True
        except Exception as ex:
            print(ex)
            return False

    def find_top_rate(self, host_id=int, limit=int):
        try:
            sql = 'select mm.rate as rate, mm.create_time as create_time from monitor_cpu as mm ' \
                  'left join monitor_cpu_host_relation as mchr on mm.id = mchr.monitor_cpu_id ' \
                  'left join host as h on h.id = mchr.host_id ' \
                  'where h.id = :host_id ' \
                  'order by mm.create_time desc ' \
                  'limit :limit'
            result = db.engine.execute(
                text(sql), {'host_id': host_id, 'limit': limit}
            )
            names = [row for row in result]
            return names
        except Exception as ex:
            return None
