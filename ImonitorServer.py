#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-03-30 11:06:00
# @Desc    : 服务器资源监控脚本
# @File    : ImonitorServer.py

import getpass
import pexpect
import re
import socket
import threading
import time
import yaml

from common.utils import CommandUtils


class MonitorServer:

    def __init__(self):
        f = open('agent.yaml')
        content = yaml.load(f)
        self.hostname = content['application']['remote']['hostname']
        if self.hostname is None:
            self.hostname = socket.gethostname()
        self.username = content['application']['remote']['username']
        if self.username is None:
            self.username = getpass.getuser()
        self.password = content['application']['remote']['password']
        self.interval = content['application']['interval']
        self.points = content['application']['points']
        f.close()

    def vm_stat(self):
        """
         统计当前节点服务器内核线程、虚拟内存、磁盘、陷阱和 CPU 活动的统计信息
        :return: 服务器状态信息
        """
        child = RemoteCommand.command_ssh_remote(self.username, self.hostname, self.password, "vmstat 1 2 | tail -n 1")
        child.expect(pexpect.EOF)
        vmstat_info = child.before.strip().split()
        processes_waiting = vmstat_info[0]
        processes_sleep = vmstat_info[1]
        swpd = vmstat_info[2]
        free = vmstat_info[3]
        buff = vmstat_info[4]
        cache = vmstat_info[5]
        si = vmstat_info[6]
        so = vmstat_info[7]
        io_bi = vmstat_info[8]
        io_bo = vmstat_info[9]
        system_interrupt = vmstat_info[10]
        system_context_switch = vmstat_info[11]
        cpu_user = vmstat_info[12]
        cpu_sys = vmstat_info[13]
        cpu_idle = vmstat_info[14]
        cpu_wait = vmstat_info[15]
        st = vmstat_info[16]
        print ('****************************内核线程、虚拟内存、磁盘、陷阱和 CPU 活动的统计信息监控****************************')
        print ("*******************时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "******************")
        print ("等待运行进程的数量:", processes_waiting)
        print ("处于不间断状态的进程:", processes_sleep)
        print ("使用虚拟内存(swap)的总量:", swpd)
        print ("空闲的内存总量:", free)
        print ("用作缓冲的内存总量:", buff)
        print ("用作缓存的内存总量:", cache)
        print ("交换出内存总量 :", si)
        print ("交换入内存总量 :", so)
        print ("从一个块设备接收:", io_bi)
        print ("发送到块设备:", io_bo)
        print ("每秒的中断数:", system_interrupt)
        print ("每秒的上下文切换数:", system_context_switch)
        print ("用户空间上进程运行的时间百分比:", cpu_user)
        print ("内核空间上进程运行的时间百分比:", cpu_sys)
        print ("闲置时间百分比:", cpu_idle)
        print ("等待IO的时间百分比:", cpu_wait)
        print ("从虚拟机偷取的时间百分比:", st)

    def disk_stat(self):
        """
        统计当前节点服务器磁盘使用信息
        :return: 磁盘信息
        """
        child = RemoteCommand.command_ssh_remote(self.username, self.hostname, self.password, "df -h")
        child.expect(pexpect.EOF)
        disk = child.before
        disklist = disk.strip().split('\n')
        disklists = []
        for disk in disklist:
            disklists.append(disk.strip().split())
        print ('************************磁盘空间监控****************************')
        print ("*******************时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "******************")
        for i in disklists[1:]:
            print ("\t文件系统：", i[0],)
            print ("\t容量：", i[1],)
            print ("\t已用：", i[2],)
            print ("\t可用：", i[3],)
            print ("\t已用%挂载点：", i[4])

    def load_stat(self):
        """
        统计当前节点服务器负载信息
        :return: 负载信息
        """
        child = RemoteCommand.command_ssh_remote(self.username, self.hostname, self.password, "cat /proc/loadavg")
        child.expect(pexpect.EOF)
        loadavgs = child.before.strip().split()
        print ('************************负载均衡监控****************************')
        print ("*******************时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "******************")
        print ("系统5分钟前的平均负载：", loadavgs[0])
        print ("系统10分钟前的平均负载：", loadavgs[1])
        print ("系统15分钟前的平均负载：", loadavgs[2])
        print ("分子是正在运行的进程数,分母为总进程数：", loadavgs[3])
        print ("最近运行的进程id：", loadavgs[4])

    def port(self):
        """
        统计当前节点服务器端口信息
        :return: 端口信息
        """
        child = RemoteCommand.command_ssh_remote(self.username, self.hostname, self.password, "netstat -tpln")
        child.expect(pexpect.EOF)
        Com = child.before
        print ('******************************端口监控*********************************')
        print ("*******************时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "******************")
        print (Com)

    def task(self):
        threads = []
        for n in range(len(self.points)):
            threads.append(threading.Thread(target=self.points[n]))
            # print '{}_info'.format(self.points[n])
            threading.Thread(target=self.points[n], args=self).start()


if __name__ == '__main__':
    MonitorServer().memory()
