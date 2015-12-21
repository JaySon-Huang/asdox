#!/usr/bin/env python
#encoding=utf-8

import unittest
from helper import BaseTestCase

class BuilderTestCase(BaseTestCase):

    def testMultipleSources(self):
        '''
        Parse multiple source files.
        '''
        self.builder.addSource(""" 
        package com.googlecode.asdox
        {
            class MyClass
            {
                
            }
        }
        """)
        self.builder.addSource(""" 
        package com.googlecode.asdox
        {
            public class MyOtherClass
            {
                
            }
        }
        """)
        pkg = self.builder.packages["com.googlecode.asdox"]
        self.assertEqual(pkg.classes["MyClass"].name, "MyClass")
        self.assertEqual(pkg.classes["MyClass"].visibility, "internal")
        self.assertEqual(pkg.classes["MyOtherClass"].name, "MyOtherClass")
        self.assertEqual(pkg.classes["MyOtherClass"].visibility, "public")

    def testAddSourceDir(self):
        '''
        Parse directory for source files
        '''
        self.builder.addSource("tests/resources/com/gurufaction")
        pkg = self.builder.packages["com.gurufaction"]
        cls1 = pkg.classes["MyClassFile1"]
        cls2 = pkg.classes["MyClassFile2"]
        self.assertEqual(cls1.name, "MyClassFile1")
        self.assertEqual(cls1.visibility, "internal")
        self.assertEqual(cls2.name, "MyClassFile2")
        self.assertEqual(cls2.visibility, "internal")
