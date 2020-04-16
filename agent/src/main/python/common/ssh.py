#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-13 15:47:50
# @Desc    : 远程连接脚本
# @File    : ssh.py

import paramiko
from StringIO import StringIO


class Ssh(object):

    def __init__(self, host, port, user, password=None, key_file=None, passphrase=None):
        pass
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

    def connect(self, hostname, port, username):
        """
        使用免密方式登录
        :param hostname: 主机名|IP地址
        :param port: 端口
        :param username: 用户名
        :return: SSH连接
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return ssh.connect(hostname=hostname, port=port, username=username, password=None, pkey=None)

    def connect_password(self, hostname, port, username, password):
        """
        使用密码方式登录
        :param hostname: 主机名|IP地址
        :param port: 端口
        :param username: 用户名
        :param password: 登录密码
        :return: SSH连接
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return ssh.connect(hostname=hostname, port=port, username=username, password=password, pkey=None)

    def connect_rsa_key(self, hostname, port, username, private_key):
        """
        使用私钥方式登录
        :param hostname: 主机名|IP地址
        :param port: 端口
        :param username: 用户名
        :param private_key: 私钥
        :return: SSH连接
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key_file = StringIO()
        private_key_file.write(private_key)
        private_key_file.seek(0)
        key = paramiko.RSAKey.from_private_key(private_key_file)
        # key = paramiko.RSAKey.from_private_key_file('/Users/shicheng/a.txt')
        return ssh.connect(hostname=hostname, username=username, port=port, pkey=key)

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
