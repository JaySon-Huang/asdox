#!/usr/bin/env python
#encoding=utf-8

import os
import sys
import unittest
sys.path.append(os.path.abspath('./'))
from asdox import asModel,asBuilder

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.builder = asBuilder.Builder()

    def tearDown(self):
        pass
