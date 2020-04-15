#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-03-30 11:06:00
# @Desc    : 服务器资源监控脚本
# @File    : monitor.py

import re

from db.models_monitor import MonitorMemory, MonitorCpu
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
            # child.expect(pexpect.EOF)
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
            # print( '******************************内存监控*********************************')
            # print( "*******************时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "******************")
            # print ("总内存：", memory_total)
            # print ("空闲内存：", memory_free)
            # print ("给文件的缓冲大小:", memory_buffers)
            # print ("高速缓冲存储器使用的大小:", memory_cached)
            # print ("被高速缓冲存储用的交换空间大小:", memory_swap_cached)
            # print ("给文件的缓冲大小:", memory_buffers)
            if 0 == int(memory_swap_total):
                # print( u"交换内存总共为：0")
                memory.swap_rate = 0
            else:
                memory_swap_rate = 100 - 100 * int(memory_swap_free) / float(memory_swap_total)
                # print(u"交换内存利用率：", memory_swap_rate)
                memory.swap_rate = memory_swap_rate
            memory_free_temp = int(memory_free) + int(memory_buffers) + int(memory_cached)
            memory_used_temp = int(memory_total) - memory_free_temp
            memory_rate = memory_used_temp / float(memory_total)
            memory.rate = round(memory_rate, 4)
            # print(u"内存利用率：", str("%.2f" % memory_rate), "%")
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
            print (ex)
            return None
