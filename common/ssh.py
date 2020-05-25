#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-13 15:47:50
# @Desc    : 远程连接脚本
# @File    : ssh.py

import io
import paramiko
from application_config import logger

StringIO = io.StringIO
from utils.string import StringUtils


class Ssh(object):

    def __init__(self, hostname='localhost', port=22, username='root', password=None, private_key=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key
        try:
            self._ssh = paramiko.SSHClient()
            self._ssh.load_system_host_keys()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if StringUtils().is_empty(source=self.password) and StringUtils().is_empty(source=self.private_key):
                logger.info('connect <%s> from <%s> by open authorization', self.hostname, self.username)
                self._ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=None,
                                  pkey=None)
            elif StringUtils().is_not_empty(source=self.password) and StringUtils().is_empty(source=self.private_key):
                logger.info('connect <%s> from <%s> by password authorization', self.hostname, self.username)
                self._ssh.connect(hostname=self.hostname, port=self.port, username=self.username,
                                  password=self.password,
                                  pkey=None)
            else:
                logger.info('connect <%s> from <%s> by private key authorization', self.hostname, self.username)
                self.private_key_file = StringIO()
                self.private_key_file.write(self.private_key)
                self.private_key_file.seek(0)
                self.key_file = self.private_key_file and paramiko.RSAKey.from_private_key(
                    self.private_key_file) or None
                self._ssh.connect(hostname=hostname, port=port, username=username, password=None, pkey=self.key_file)
            self._chanel = self._ssh.invoke_shell(term='xterm')
            self.connected = True
            logger.info('from <%s> by <%s> connected', self.hostname, self.username)
        except Exception as ex:
            logger.error('connect <%s> from <%s> Authentication failed')
            self.message = ex
            self.connected = False

    def connect(self, hostname, port, username):
        """
        使用免密方式登录
        :param hostname: 主机名|IP地址
        :param port: 端口
        :param username: 用户名
        :return: SSH连接
        """
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(hostname=hostname, port=port, username=username, password=None, pkey=None)

    def connect_password(self, hostname, port, username, password):
        """
        使用密码方式登录
        :param hostname: 主机名|IP地址
        :param port: 端口
        :param username: 用户名
        :param password: 登录密码
        :return: SSH连接
        """
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(hostname=hostname, port=port, username=username, password=password, pkey=None)

    def connect_rsa_key(self, hostname, port, username, private_key):
        """
        使用私钥方式登录
        :param hostname: 主机名|IP地址
        :param port: 端口
        :param username: 用户名
        :param private_key: 私钥
        :return: SSH连接
        """
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key_file = StringIO()
        private_key_file.write(private_key)
        private_key_file.seek(0)
        key = paramiko.RSAKey.from_private_key(private_key_file)
        self._ssh.connect(hostname=hostname, username=username, port=port, pkey=key)

    def resize(self, cols, rows):
        """
        重置窗口大小
        """
        if self.connected:
            self._chanel.resize_pty(width=cols, height=rows)
        else:
            logger.error('not connected from <%s> by <%s>', self.hostname, self.username)

    def send(self, message):
        self._chanel.send(message)

    def read(self):
        context = self._chanel.recv(10000)
        return context

    def get_connect(self):
        return self._ssh

    def get_message(self):
        return self.message

    def check_connect(self):
        if self.connected:
            self._chanel.close()
            self._ssh.close()
            return True
        else:
            return False

    def close(self):
        if self.connected:
            self._chanel.close()
            self._ssh.close()


if __name__ == '__main__':
    print(Ssh(hostname='localhost', port=22, username='root', password='123456', private_key=None))
    print('------ 使用免密方式登录服务器 ------')
    print(Ssh().connect('localhost', 22, 'root'))
    print('------ 使用密码方式登录服务器 ------')
    print(Ssh().connect_password('localhost', 22, 'root', '123456'))
    print('------ 使用私钥方式登录服务器 ------')
    private = '''-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA9QlpIHDowlUDzNH95VMGjc9kpQXFoQXup/sfGRDjhgxiydYI
ZvupNi58LsSdJdm4RUSiiTu8RECVupNqrcJrVn2HM0kMSwpkvXqasBE+f+EWn4pM
+Xb8z7otpAanejK5QMNONvlVDfPRmawTQ/aDEKZjpuTv5SkjTZNj7WGYHuA6aHOX
eF00YnFGrHV479Y0I1IlnH4EFgKEtCqRaUeV5WfNW0bAhMcqnBd54R3NIp3RAMp3
+pzxOrulDLH5BPSeATB18Q6DkrAvDMinqucd+RxfIXQmk4acIF/+azO2glnvoklt
iUIMu8sCtgLdRebJX5Ce+ivihTAK5sSQ6aLyhwIDAQABAoIBAGUZnOZlr6N+sDKx
8a/MsceQ6lWsK/5kFDP6yLnu3fFQ6vGb/Zt/+jEAvPwO40farMznpKg6nVML0rtI
V5uZu+/TmxTt7sSHZUlIbMp4UvEwTcVFqrzC+0w55NroY/FnPEgcTQkhlpZLIw/k
j45bB3i3LiaODuzeLFK1nWUz/y+9Ra6y9aYPrkGiMrriZdGCiwxPqUMVJnDCryg6
rn3soL/d3LbscZ+CLIK26swoU65KMaa1bDhtiICfRSbgFBZyUnUijiT7W76GPLTF
kUnP5VClohj2QI+UmmVgiXfKEdmBxlfsd1ujOtcNKvq8nJJX4WHafPt9PfYUc9Yc
pjGvwgECgYEA+sI4f/w28+fCHz+Oztj7q+7Xkb6AZa7arQVWQ647jYCg8S/tIgws
HjopIZ0WpvTS2k3DjJ38KDQVJtP+PQNvEppOQRNJd6PAEbfbJw8w8tfjUHbCMjg0
8VgqHtwtymScVZYrYXaza2+s/5xpYY4ykw+GZW89cCvz5ctdxoykQN8CgYEA+iiS
mwj5hkx6jKQkdhhKDatJ5mW7LkCX8B6HIxVf9wG49NCtwraGVVlqbgy1WhLZgZjn
1qEn5V6823l8VzXfcF4zq9uPHPT6ddfIyXnE3sdxiHgsaT5Wa4VN+CvFTQdwWUYb
epNdpBP+fDVmXZVGqEjO2x1QqtGjXCU+OqALO1kCgYA+wuvHRMYwR9pzXcINjYt4
HgCAbvDOAnSjB4nuyKYJJZ+inj843VkRe7cdvaaUxQQdNYdzI3ugSGDe5gJlHP3o
5wwdB4nE0wxYou7MGOZEcbpoQkEatqyxl0J7lNo1JPdoCHz1GPOROVNQasKJc0C/
RAx8SNpUv/t8kWj4L+1QewKBgAssKrgP440S91o2roYzuYL4xnkqy/xZ2C9aPbDc
cIfIpOkSNOCAZGmFb9JwcN0QAHTgTmJwmiaNX6PxvhLrDgqnumkPiknByzneJFKT
RK6qe7CbpWgh55wvvPa7hblV/reOAQYtdL4yQmhrviGp3BkB/3Mb0RGAAWrJIwld
QoMpAoGAZTNv/JIL8uR2tMtOXEhPwEJkfdSE/VyZrNwt9/vS8gfw6skFMpoFm+JM
ic5ZOwSOCen+6+Hh4yj0PtmpkGoCA8RsI0u3HZNNWjP4LiSJJZSGUkwOYEQfkz20
no9eNaBC4uqP/XTU9KAnOeEDE/hV190X21DtNNq5a6nWBZqZveI=
-----END RSA PRIVATE KEY-----'''
    print(Ssh().connect_rsa_key('localhost', 22, 'root', private))
