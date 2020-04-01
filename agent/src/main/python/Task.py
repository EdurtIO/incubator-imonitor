#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-03-30 15:14:47
# @Desc    : 任务
# @File    : Task.py
import threading

import ImonitorServer


class TaskThread(threading.Thread):  # 继承父类threading.Thread

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        monitor = ImonitorServer.MonitorServer()
        monitor.task()


# 创建新线程
thread1 = TaskThread(1, "Thread-1", 1)

# 开启线程
thread1.start()

print("Exiting Main Thread")
