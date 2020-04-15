#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-13 15:47:50
# @Desc    : 远程连接脚本
# @File    : ssh.py

import paramiko


class Ssh(object):

    def __init__(self, host, port, user, password=None, key_file=None, passphrase=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.key_file = key_file
        self._ssh = paramiko.SSHClient()
        self._ssh.load_system_host_keys()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        k = key_file and paramiko.RSAKey.from_private_key_file(
            key_file, password=passphrase) or None
        self._ssh.connect(hostname=host, port=port, username=user,
                          password=password, pkey=k)
        self._chanel = self._ssh.invoke_shell(
            term='xterm')

    def resize(self, cols, rows):
        """
        重置窗口大小
        """
        self._chanel.resize_pty(width=cols, height=rows)

    def send(self, msg):
        self._chanel.send(msg)

    def read(self):
        return self._chanel.recv(10000)


if __name__ == '__main__':
    Ssh(host='10.10.0.90', password='', port='22', user='root')
