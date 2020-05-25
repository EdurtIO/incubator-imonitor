#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @User    : shicheng
# @Date    : 2020-05-25 22:29
# @File    : test_string.py
import unittest

from utils.string import StringUtils


class TestStringUtils(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    self._str_0 = ''
    self._str_1 = '1'

  def test_is_empty(self):
    self.assertTrue(StringUtils.is_empty(self._str_0))
    self.assertFalse(StringUtils.is_empty(self._str_1))

  def test_is_not_empty(self):
    self.assertFalse(StringUtils.is_not_empty(self._str_0))
    self.assertTrue(StringUtils.is_not_empty(self._str_1))
