#!/usr/bin/env python
#encoding=utf-8

import unittest
from helper import BaseTestCase

class ASClassTestCase(BaseTestCase):
    def testClass(self):
        self.builder.addSource("""
        package com.gurufaction.mypackage
        {
            public class MyBasicClass
            {

            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.mypackage"]
        cls = pkg.classes["MyBasicClass"]
        self.assertEqual(cls.name, "MyBasicClass")
        self.assertEqual(cls.visibility, "public")

    def testClassMetadataJavaDocComment(self):
        self.builder.addSource("""
        package test
        {
            /**
            *  Dispatched when the user presses the Button control.
            *  If the <code>autoRepeat</code> property is <code>true</code>,
            *  this event is dispatched repeatedly as long as the button stays down.
            *
            *  @eventType mx.events.FlexEvent.BUTTON_DOWN
            */

            [Event(name="buttonDown", type="mx.events.FlexEvent")]
            public class MyClass
            {
            }
        }
        """)
        pkg = self.builder.packages["test"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.name, "MyClass")
        self.assertEqual(cls.visibility, "public")
        self.assertEqual(cls.metadata[0].name, "Event")
        self.assertEqual(
            cls.metadata[0].params,
            {'type': 'mx.events.FlexEvent', 'name': 'buttonDown'}
        )

    def testClassMetaData(self):
        self.builder.addSource("""
        package test{
            [Bindable]
            [Event(name="myEnableEvent", type="flash.events.Event")]
            [DefaultTriggerEvent("click")]
            public class MyClass
            {
            }
        }
        """)
        # Test Package 'test'
        pkg = self.builder.packages["test"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.name, "MyClass")
        self.assertEqual(cls.visibility, "public")
        self.assertEqual(cls.metadata[0].name, "Bindable")
        self.assertEqual(cls.metadata[0].params, {})
        self.assertEqual(cls.metadata[1].name, "Event")
        self.assertEqual(
            cls.metadata[1].params,
            {'name': 'myEnableEvent', 'type':'flash.events.Event'}
        )
        self.assertEqual(cls.metadata[2].name, "DefaultTriggerEvent")
        self.assertEqual(cls.metadata[2].params, {0: 'click'})


    def testClassInclude(self):
        '''Parse Class with Include statement'''
        self.builder.addSource("""
        package com.gurufaction.mypackage
        {
            public class MyClass
            {
                include "../core/Version.as";
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.mypackage"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.name, "MyClass")
        self.assertEqual(cls.visibility, "public")

    def testClassExtends(self):
        '''Parse Class with Extends'''
        self.builder.addSource("""
        package com.gurufaction.mypackage
        {
            public class MyClass extends BaseClass
            {
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.mypackage"]
        self.assertEqual(pkg.classes["MyClass"].name, "MyClass")
        self.assertEqual(pkg.classes["MyClass"].extends, "BaseClass")
        self.assertEqual(pkg.classes["MyClass"].visibility, "public")

    def testClassImplements(self):
        '''Parse Class which implements interfaces'''
        self.builder.addSource("""
        package com.gurufaction.mypackage
        {
            public class MyClass implements IWorkable, ITestable
            {
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.mypackage"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.implements[0], "IWorkable")
        self.assertEqual(cls.implements[1], "ITestable")

    def testInternalClassModifier(self):
        '''Parse for 'internal' class modifier'''
        self.builder.addSource("""
        package
        {
            class MyClass
            {
            }
        }
        """)
        pkg = self.builder.packages[""]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.visibility, "internal")

    def testPublicClassModifier(self):
        '''Parse for 'public' class modifier'''
        self.builder.addSource("""
        package
        {
            public class MyClass
            {
            }
        }
        """)
        pkg = self.builder.packages[""]
        self.assertEqual(pkg.classes["MyClass"].visibility, "public")

    def testDynamicClassModifier(self):
        '''Parse for 'dynamic' class modifier'''
        self.builder.addSource("""
        package
        {
            dynamic class MyClass
            {
            }
        }
        """)
        pkg = self.builder.packages[""]
        self.assertEqual(pkg.classes["MyClass"].isDynamic, True)

    def testFinalClassModifier(self):
        '''Parse for 'final' class modifier'''
        self.builder.addSource("""
        package
        {
            final class MyClass
            {
            }
        }
        """)
        pkg = self.builder.packages[""]
        self.assertEqual(pkg.classes["MyClass"].isFinal,True)

    def testDynamicFinalClassModifier(self):
        '''Parse for 'dynamic final' class modifier'''
        self.builder.addSource("""
        package
        {
            dynamic final class MyClass
            {
            }
        }
        """)
        pkg = self.builder.packages[""]
        self.assertEqual(pkg.classes["MyClass"].isDynamic,True)
        self.assertEqual(pkg.classes["MyClass"].isFinal,True)
