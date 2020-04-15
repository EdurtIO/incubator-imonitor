#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 18:45:26
# @Desc    : host数据服务
# @File    : service_host.py

from sqlalchemy import desc, text

from application_config import db
from db.models_monitor import MonitorMemory


class MonitorMemoryService:

    def find_all(self):
        return MonitorMemory().query.all()

    def find_one(self, id=int):
        return MonitorMemory().query.filter_by(id=id).first()

    def find_all_order_by_create_time_desc(self):
        return MonitorMemory().query.order_by(desc(Host.create_time)).all()

    def add(self, monitor_memory=MonitorMemory, host_id=int):
        try:
            db.session.add(monitor_memory)
            db.session.flush()
            db.session.commit()
            sql = 'insert into monitor_memory_host_relation(host_id, monitor_memory_id) ' \
                  'values(:host_id, :monitor_memory_id)'
            db.engine.execute(
                text(sql), {'host_id': host_id, 'monitor_memory_id': monitor_memory.id}
            )
            return True
        except Exception as ex:
            print(ex)
            return False

    def find_top_15(self, host_id=int):
        try:
            sql = 'select mm.total as total, mm.free as free, mm.buffers as buffers, mm.cached as cached, mm.swap_cached as swap_cached, mm.swap_total as swap_total, mm.swap_free as swap_free, mm.swap_rate as swap_rate, mm.rate as rate, mm.create_time as create_time from monitor_memory as mm ' \
                  'left join monitor_memory_host_relation as mmhr on mm.id = mmhr.monitor_memory_id ' \
                  'left join host as h on h.id = mmhr.host_id ' \
                  'where h.id = :host_id ' \
                  'order by mm.create_time desc ' \
                  'limit 15'
            result = db.engine.execute(
                text(sql), {'host_id': host_id}
            )
            names = [row for row in result]
            return names
        except Exception as ex:
            return None

    def find_top_rate(self, host_id=int, limit=int):
        try:
            sql = 'select mm.rate as rate, mm.create_time as create_time from monitor_memory as mm ' \
                  'left join monitor_memory_host_relation as mmhr on mm.id = mmhr.monitor_memory_id ' \
                  'left join host as h on h.id = mmhr.host_id ' \
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

