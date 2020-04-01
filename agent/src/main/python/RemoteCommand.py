#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-03-30 11:30:15
# @Desc    : 服务器远程操作脚本
# @File    : RemoteCommand.py

import logging
import pexpect


def command_ssh_remote(user, host, password, command):
    """
    远程连接服务器
    :param user: 服务器用户名称
    :param host: 服务器主机地址
    :param password: 服务器用户密码 TODO: 后期支持
    :param command: 需要执行的命令
    :return: 命令执行结果
    """
    logging.debug('开始登录服务器:%s 登录用户：%s 执行命令：%s', host, user, command)
    # print command
    child = pexpect.spawn("ssh -l %s %s '%s'" % (user, host, command))
    return child
