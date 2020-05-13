#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-03-30 11:06:00
# @Desc    : 服务器资源监控脚本
# @File    : monitor.py

import re
from application_config import logger
from db.models_monitor import MonitorMemory, MonitorCpu, MonitorNetworkIO

from .utils import CommandUtils


class MonitorUtils:

    def memory(self, username, hostname, password):
        """
        统计当前节点服务器内存状态
        :return: 内存详细信息
        """
        try:
            memory = MonitorMemory()
            child = CommandUtils().command_ssh_remote_password(username, hostname, password, "cat /proc/meminfo")
            memory_values = re.findall("(\d+)\ kB", str(child.before))
            memory_total = memory_values[0]
            memory_free = memory_values[1]
            memory_buffers = memory_values[2]
            memory_cached = memory_values[3]
            memory_swap_cached = memory_values[4]
            memory_swap_total = memory_values[13]
            memory_swap_free = memory_values[14]
            memory.total = memory_total
            memory.free = memory_free
            memory.buffers = memory_buffers
            memory.cached = memory_cached
            memory.swap_cached = memory_swap_cached
            memory.swap_total = memory_swap_total
            memory.swap_free = memory_swap_free
            if 0 == int(memory_swap_total):
                memory.swap_rate = 0
            else:
                memory_swap_rate = 100 - 100 * int(memory_swap_free) / float(memory_swap_total)
                memory.swap_rate = memory_swap_rate
            memory_free_temp = int(memory_free) + int(memory_buffers) + int(memory_cached)
            memory_used_temp = int(memory_total) - memory_free_temp
            memory_rate = memory_used_temp / float(memory_total)
            memory.rate = round(memory_rate, 4)
            return memory
        except Exception as ex:
            print (ex)
            return None

    def cpu(self, username, hostname, password):
        """
        统计当前节点服务器CPU信息
        :return: CPU信息
        """
        try:
            cpu = MonitorCpu()
            child = CommandUtils().command_ssh_remote_password(username, hostname, password,
                                                               'cat /proc/stat | grep "cpu "')
            child1 = CommandUtils().command_ssh_remote_password(username, hostname, password,
                                                                'cat /proc/stat | grep "cpu "')
            cpus = child.before.strip().split()
            cpus1 = child1.before.strip().split()
            T1 = int(cpus[1]) + int(cpus[2]) + int(cpus[3]) + int(cpus[4]) + int(cpus[5]) + int(cpus[6]) + int(
                cpus[8]) + int(
                cpus[9])
            T2 = int(cpus1[1]) + int(cpus1[2]) + int(cpus1[3]) + int(cpus1[4]) + int(cpus1[5]) + int(cpus1[6]) + int(
                cpus1[8]) + int(cpus1[9])
            Tol = T2 - T1
            Idle = int(cpus1[4]) - int(cpus[4])
            cpu.cpu_time_1 = T1
            cpu.cpu_time_2 = T2
            cpu.idle = Idle
            cpu.rate = round((Tol - Idle) / Tol, 4)
            return cpu
        except Exception as ex:
            print(ex)
            return None

    def network_io(self, username, hostname, password):
        """
        统计当前节点服务器网络IO信息
        :return: 网络IO信息
        """
        try:
            logger.info('connect <%s> from <%s>', hostname, username)
            child = CommandUtils().command_ssh_remote_password(username, hostname, password, "cat /proc/net/dev")
            logger.info('from <%s> by <%s> connected', hostname, username)
            temp = child.before.decode().strip().split('\n')
            nios = []
            for line in temp[2:]:
                network_io = MonitorNetworkIO()
                line = line.split(":")
                network_io.name = line[0].strip()
                network_io.receive = round(float(line[1].split()[0]) / (1024.0 * 1024.0), 2)
                network_io.transmit = round(float(line[1].split()[8]) / (1024.0 * 1024.0), 2)
                nios.append(network_io)
            return nios
        except Exception as ex:
            logger.error('connect <%s> from <%s> failure, reason <%s>', hostname, username, ex)
            return None
