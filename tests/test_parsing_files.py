#!/usr/bin/env python
# encoding=utf-8

import unittest
from helper import BaseTestCase


class ParsingExternalFileTestCase(BaseTestCase):
    def testFilterClassFile(self):
        '''
        Load and Parse Filter.as source file.
        '''
        self.builder.addSource("tests/resources/Filter.as")
        self.builder.addSource("tests/resources/Filter2.as")
        pkg = self.builder.packages["com.franklinconnections"]
        self.assertEqual(
            list(map(lambda imp: imp.name, pkg.imports)),
            [
                'mx.collections.ArrayCollection',
                'mx.controls.Alert',
                'com.foo2',
                'com.foo3'
            ]
        )
        self.assertEqual(pkg.classes["Filter"].name, "Filter")

    @unittest.skip("FIXME: include statements")
    def testButtonClassFile(self):
        '''
        Load and Parse Button.as source file.
        FIXME: include statements
        FIXME: 错误 override public function set enabled(value:Boolean):void
        '''
        self.builder.addSource("tests/resources/Button.as")
        pkg = self.builder.packages["mx.controls"]
        self.assertEqual(pkg.classes["Button"].name, "Button")

    def testUTF8ClassFile(self):
        '''
        Load and Parse UTF-8 source file.
        '''
        self.builder.addSource("tests/resources/mx/utils/StringUtil.as")
        pkg = self.builder.packages["mx.utils"]
        self.assertEqual(pkg.classes["StringUtil"].name, "StringUtil")
