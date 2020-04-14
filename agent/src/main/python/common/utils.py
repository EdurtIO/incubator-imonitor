#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 16:30:15
# @Desc    : 全局工具类脚本
# @File    : utils.py


class NumberUtils:

    def is_number(self, content):
        """
        判断数据是否是数值类型
        :param content: 数据
        :return: True|False
        """
        if content is None:
            return False
        try:
            float(content)
            return True
        except ValueError:
            return False


class DirctoryUtils:

    def get_attr_by_key(self, content, key):
        """
        根据提供的key获取属性值
        :param content: 源数据
        :param key: key
        :return: 属性值，默认为None
        """
        value = None
        if key is '':
            print('无效的主键')
        else:
            try:
                value = content[key]
            except Exception:
                value = None
        return value


import logging
import pexpect


class CommandUtils:

    def command_ssh_remote(self, user, host, password, command):
        """
        远程连接服务器
        :param user: 服务器用户名称
        :param host: 服务器主机地址
        :param password: 服务器用户密码 TODO: 后期支持
        :param command: 需要执行的命令
        :return: 命令执行结果
        """
        buffer = None
        try:
            logging.debug('开始登录服务器:%s 登录用户：%s 执行命令：%s', host, user, command)
            child = pexpect.spawn("ssh -o stricthostkeychecking=no -l %s %s '%s'" % (user, host, command), timeout=5)
            buffer = child
            child.expect(pattern=pexpect.EOF, timeout=10)
            buffer = child
        except Exception:
            print(buffer)
        finally:
            child.close()
        return buffer

    def command_ssh_remote_password(self, user, host, password, command):
        """
        远程连接服务器
        :param user: 服务器用户名称
        :param host: 服务器主机地址
        :param password: 服务器用户密码
        :param command: 需要执行的命令
        :return: 命令执行结果
        """
        buffer = None
        try:
            logging.debug('开始登录服务器:%s 登录用户：%s 执行命令：%s', host, user, command)
            child = pexpect.spawn("ssh -o stricthostkeychecking=no -l %s %s '%s'" % (user, host, command), timeout=5)
            try:
                child_pw = child.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
                if child_pw == 0:
                    child.sendline(password)
                elif child_pw == 1:
                    child.sendline('yes\n')
                    child.expect('password: ')
                    child.sendline(password)
                child.sendline(command)
                child.expect(pattern=pexpect.EOF, timeout=10)
                buffer = child
            except pexpect.EOF:
                child.close()
            except pexpect.TIMEOUT:
                child.close()
        except Exception:
            print(' ====== ')
        return buffer


if __name__ == '__main__':
    CommandUtils().command_ssh_remote_password('root', '127.0.0.1', '123456', 'ls -l')
    print(NumberUtils().is_number('12123s'))
