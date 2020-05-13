#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-04-03 16:11:37
# @Desc    : Open FaIcon插件推送
# @File    : FaIconPush.py

import calendar
import json
import logging
import requests
import time

FORMAT = '%(asctime)-15s - %(message)s'
logging.basicConfig(format=FORMAT)


class FaIcon:

    def __init__(self):
        logging.debug('init FaIcon param starting')
        self.remote = 'http://127.0.0.1:1988/v1/push'
        logging.debug('FaIcon remote http address is %s', self.remote)
        logging.debug('init FaIcon param stop')

    def build_data(self, source):
        if source is None or source is '':
            logging.error('source data is None or \'\', build is exit')
            return
        json_data = json.loads(source)
        push_datas = []
        for temp in json_data:
            model = {}
            model['endpoint'] = temp['service_host']
            model['value'] = temp['service_code']
            model['metric'] = 'idc.druid.{}'.format(temp['service_name'])
            model['tags'] = 'idc=idc,project=druid_{}_heartbeat'.format(temp['service_name'])
            model['step'] = 60
            model['timestamp'] = calendar.timegm(time.gmtime())
            model['counterType'] = 'GAUGE'
            push_datas.append(model)
        return push_datas

    def push(self, source):
        push_data = self.build_data(source)
        headers = {"Content-Type": "application/json"}
        r = requests.post(self.remote, data=json.dumps(push_data), headers=headers)
        print(r)


if __name__ == '__main__':
    FaIcon().push()
