#!/usr/bin/env python
#encoding=utf-8

import unittest
from helper import BaseTestCase

class ASFieldTestCase(BaseTestCase):
    def testClassField(self):
        '''
        Parse class field.
        '''
        self.builder.addSource(""" 
        package 
        {
            class MyClass
            {
                internal var today:DateTime;
            }
        }
        """)
        pkg = self.builder.packages[""]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.name, "MyClass")
        self.assertEqual(cls.visibility, "internal")

        self.assertEqual(cls.variables["today"].name, "today")
        self.assertEqual(cls.variables["today"].type_, "DateTime")
        self.assertEqual(cls.variables["today"].visibility, "internal")

    def testConstantClassField(self):
        '''
        Parse class constant field.
        '''
        self.builder.addSource(""" 
        package 
        {
            class MyClass
            {
                internal const PI:Number;
            }
        }
        """)
        pkg = self.builder.packages[""]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.name, "MyClass")
        self.assertEqual(cls.visibility, "internal")

        self.assertEqual(cls.variables["PI"].name, "PI")
        self.assertEqual(cls.variables["PI"].type_, "Number")
        self.assertEqual(cls.variables["PI"].visibility, "internal")
        self.assertEqual(cls.variables["PI"].isConstant, True)

    def testStaticClassField(self):
        '''
        Parse class static field.
        '''
        self.builder.addSource(""" 
        package 
        {
            class MyClass
            {
                internal static var count:int;
            }
        }
        """)
        pkg = self.builder.packages[""]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.variables["count"].name, "count")
        self.assertEqual(cls.variables["count"].type_, "int")
        self.assertEqual(cls.variables["count"].visibility, "internal")
        self.assertEqual(cls.variables["count"].isConstant, False)
        self.assertEqual(cls.variables["count"].isStatic, True)

    def testFieldModifiers(self):
        '''
        Parse field modifiers
        '''
        self.builder.addSource(""" 
        package
        {
            class MyClass
            {
                public var name:String;
                private var age:int;
                protected var salary:Number;
            }
        }
        """)
        pkg = self.builder.packages[""]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.name, "MyClass")
        self.assertEqual(cls.visibility, "internal")

        self.assertEqual(cls.variables["name"].name, "name")
        self.assertEqual(cls.variables["name"].type_, "String")
        self.assertEqual(cls.variables["name"].visibility, "public")
        self.assertEqual(cls.variables["name"].isConstant, False)

        self.assertEqual(cls.variables["age"].name, "age")
        self.assertEqual(cls.variables["age"].type_, "int")
        self.assertEqual(cls.variables["age"].visibility, "private")
        self.assertEqual(cls.variables["age"].isConstant, False)

        self.assertEqual(cls.variables["salary"].name, "salary")
        self.assertEqual(cls.variables["salary"].type_, "Number")
        self.assertEqual(cls.variables["salary"].visibility, "protected")
        self.assertEqual(cls.variables["salary"].isConstant, False)

    def testFieldInitialization(self):
        '''
        Parse field initialization
        '''
        self.builder.addSource(""" 
        package
        {
            class MyClass
            {
                internal var name:String = "Michael Ramriez";
                internal var age:int = 29;
                internal var salary:Number = 41000.52;
                internal var isSmart:Boolean = True;
                internal var _labelPlacement:String = ButtonLabelPlacement.RIGHT; 
            }
        }
        """)
        pkg = self.builder.packages[""]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.name, "MyClass")
        self.assertEqual(cls.visibility, "internal")

        self.assertEqual(cls.variables["name"].name, "name")
        self.assertEqual(cls.variables["name"].type_, "String")
        self.assertEqual(cls.variables["name"].visibility, "internal")
        self.assertEqual(cls.variables["name"].isConstant, False)

        self.assertEqual(cls.variables["age"].name, "age")
        self.assertEqual(cls.variables["age"].type_, "int")
        self.assertEqual(cls.variables["age"].visibility, "internal")
        self.assertEqual(cls.variables["age"].isConstant, False)

        self.assertEqual(cls.variables["salary"].name, "salary")
        self.assertEqual(cls.variables["salary"].type_, "Number")
        self.assertEqual(cls.variables["salary"].visibility, "internal")
        self.assertEqual(cls.variables["salary"].isConstant, False)

        self.assertEqual(cls.variables["isSmart"].name, "isSmart")
        self.assertEqual(cls.variables["isSmart"].type_, "Boolean")
        self.assertEqual(cls.variables["isSmart"].visibility, "internal")
        self.assertEqual(cls.variables["isSmart"].isConstant, False)

        self.assertEqual(cls.variables["_labelPlacement"].name, "_labelPlacement")
        self.assertEqual(cls.variables["_labelPlacement"].type_, "String")
        self.assertEqual(cls.variables["_labelPlacement"].visibility, "internal")
        self.assertEqual(cls.variables["_labelPlacement"].isConstant, False)

    def testFieldNamespaceModifier(self):
        '''
        Parse class namespace modifier
        '''
        self.builder.addSource(""" 
        package
        {
            class MyClass
            { 
                mx_internal var name:String;
            }
        }
        """)
        pkg = self.builder.packages[""]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.name, "MyClass")
        self.assertEqual(cls.visibility, "internal")

        self.assertEqual(cls.variables["name"].name, "name")
        self.assertEqual(cls.variables["name"].type_, "String")
        self.assertEqual(cls.variables["name"].visibility, "mx_internal")
        self.assertEqual(cls.variables["name"].isConstant, False)   

    @unittest.skip("FIXME: metadatas of variable")
    def testMetaDataWithClassFields(self):
        '''
        Parse class Fields with metadata
        '''
        self.builder.addSource(""" 
        package
        {
            class MyClass
            { 
                [Bindable]
                mx_internal var name:String;
            }
        }
        """)
        pkg = self.builder.packages[""]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.name, "MyClass")
        self.assertEqual(cls.visibility, "internal")

        self.assertEqual(cls.variables["name"].name, "name")
        self.assertEqual(cls.variables["name"].type_, "String")
        self.assertEqual(cls.variables["name"].visibility, "mx_internal")
        self.assertEqual(cls.variables["name"].isConstant, False)
        self.assertEqual(cls.variables["name"].metadata[0].name, "Bindable")
        self.assertEqual(cls.variables["name"].metadata[0].params, {})
