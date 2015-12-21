#!/usr/bin/env python
#encoding=utf-8

import unittest
from helper import BaseTestCase

class ASMethodTestCase(BaseTestCase):
    "Test cases for class methods"

    def testConstructorMethod(self):
        '''
        Parse class constructor method with no arguments.
        '''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                public function MyClass()
                {
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.name, "MyClass")
        self.assertEqual(cls.visibility, "public")
        self.assertEqual(cls.methods["MyClass"].name, "MyClass")
        self.assertEqual(cls.methods["MyClass"].visibility, "public")

    def testMethod(self):
        '''
        Parse class method with no arguments.
        '''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                public function sayHi():String
                {
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.methods["sayHi"].name, "sayHi")
        self.assertEqual(cls.methods["sayHi"].visibility, "public")

    def testMethodOverriding(self):
        '''Parse overridden class method'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            class MyClass
            {
                public override function thanks():String 
                {
                    return super.thanks() + " nui loa";
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.methods["thanks"].name, "thanks")
        self.assertEqual(cls.methods["thanks"].type_, "String")
        self.assertEqual(cls.methods["thanks"].visibility, "public")
        self.assertEqual(cls.methods["thanks"].isOverride, True)

    def testMethodArguments(self):
        '''Parse class method with multiple arguments.'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                public function addIntegers(num1:int,num2:int):int
                {
                    return num1 + num2;
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.methods["addIntegers"].name, "addIntegers")
        self.assertEqual(cls.methods["addIntegers"].type_, "int")
        self.assertEqual(cls.methods["addIntegers"].visibility, "public")
        self.assertEqual(cls.methods["addIntegers"].isOverride, False)
        self.assertEqual(cls.methods["addIntegers"].arguments["num1"].name, "num1")
        self.assertEqual(cls.methods["addIntegers"].arguments["num1"].type_, "int")
        self.assertEqual(cls.methods["addIntegers"].arguments["num2"].name, "num2")
        self.assertEqual(cls.methods["addIntegers"].arguments["num2"].type_, "int")

    def testMethodMultiLineComment(self):
        '''Parse class method with multi-line comment.'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                /*
                * Method returns empty string
                */
                public function getName():String
                {
                    return "";
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.methods["getName"].name, "getName")
        self.assertEqual(cls.methods["getName"].type_, "String")
        self.assertEqual(cls.methods["getName"].visibility, "public")
        self.assertEqual(cls.methods["getName"].isOverride, False)

    def testMethodSingleLineComment(self):
        '''Parse class method with single-line comment.'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                // Method returns empty string
                public function getName():String
                {
                    return "";
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.methods["getName"].name, "getName")
        self.assertEqual(cls.methods["getName"].type_, "String")
        self.assertEqual(cls.methods["getName"].visibility, "public")
        self.assertEqual(cls.methods["getName"].isOverride, False)

    @unittest.skip('FIXME: multiple metadatas')
    def testMethodMetadata(self):
        '''Parse class method with metadata comment.'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                [Bindable("dataChange")]
                [Inspectable(environment="none")]
                public function getName():String
                {
                    return "";
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.methods["getName"].name, "getName")
        self.assertEqual(cls.methods["getName"].type_, "String")
        self.assertEqual(cls.methods["getName"].visibility, "public")
        self.assertEqual(cls.methods["getName"].isOverride, False)
        self.assertEqual(cls.methods["getName"].metadata[0].name, "Inspectable")
        self.assertEqual(
            cls.methods["getName"].metadata[0].params,
            {'environment': 'none'}
        )
        self.assertEqual(
            cls.methods["getName"].metadata[1].name,
            "Bindable"
        )
        self.assertEqual(
            cls.methods["getName"].metadata[1].params,
            {0: 'dataChange'}
        )

    @unittest.skip('FIXME: getter')
    def testMethodGetter(self):
        '''Parse class method with getter.'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                public function get labelPlacement():String
                {
                    return _labelPlacement;
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.variables["labelPlacement"].name, "labelPlacement")
        self.assertEqual(cls.variables["labelPlacement"].type_, "String")
        self.assertEqual(cls.variables["labelPlacement"].visibility, "public")
        self.assertEqual(cls.variables["labelPlacement"].readable, True)
        self.assertEqual(cls.variables["labelPlacement"].writable, False)
        self.assertEqual(cls.variables["labelPlacement"].isProperty, True)

    @unittest.skip('FIXME: setter')
    def testMethodSetter(self):
        '''Parse class method with setter.'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                public function set labelPlacement(label:String):void
                {
                    _labelPlacement = label;
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.variables["labelPlacement"].name, "labelPlacement")
        self.assertEqual(cls.variables["labelPlacement"].type_, "String")
        self.assertEqual(cls.variables["labelPlacement"].visibility, "public")
        self.assertEqual(cls.variables["labelPlacement"].readable, False)
        self.assertEqual(cls.variables["labelPlacement"].writable, True)
        self.assertEqual(cls.variables["labelPlacement"].isProperty, True)

    @unittest.skip('FIXME: getter/setter')
    def testMethodGetterAndSetter(self):
        '''Parse class method with setter and getter.'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                public function get name():String
                {
                    return _name;
                }
                
                public function set name(name:String):void
                {
                    _name = name;
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.variables["name"].name, "name")
        self.assertEqual(cls.variables["name"].type_, "String")
        self.assertEqual(cls.variables["name"].visibility, "public")
        self.assertEqual(cls.variables["name"].readable, True)
        self.assertEqual(cls.variables["name"].writable, True)
        self.assertEqual(cls.variables["name"].isProperty, True)

    def testMethodNamespace(self):
        '''
        Parse class method with namespace.
        '''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                mx_internal function setSelected(value:Boolean):void
                {
                    if (_selected != value)
                    {
                        _selected = value;

                        invalidateDisplayList();
    
                        if (toggle)
                            dispatchEvent(new Event(Event.CHANGE));

                        dispatchEvent(new FlexEvent(FlexEvent.VALUE_COMMIT));
                    }
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.methods["setSelected"].name, "setSelected")
        self.assertEqual(cls.methods["setSelected"].type_, "void")
        self.assertEqual(cls.methods["setSelected"].visibility, "mx_internal")
        self.assertEqual(cls.methods["setSelected"].isOverride, False)
        self.assertEqual(
            cls.methods["setSelected"].arguments["value"].name,
            "value"
        )
        self.assertEqual(
            cls.methods["setSelected"].arguments["value"].type_,
            "Boolean"
        )
