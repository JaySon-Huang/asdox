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

    def testConstructorMethodWithOneArguments(self):
        self.builder.addSource('''
        package com.gurufaction.asdox {
            import flash.net.*;
            public dynamic class ModelPanel extends Item {

                private var modelDesTA:TextArea;

                public function ModelPanel(scale:Number){
                }
            }
        }
        ''')
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["ModelPanel"]
        self.assertEqual(cls.name, 'ModelPanel')
        self.assertEqual(cls.visibility, 'public')
        self.assertEqual(cls.methods['ModelPanel'].name, 'ModelPanel')
        self.assertEqual(cls.methods['ModelPanel'].visibility, 'public')
        arg = cls.methods['ModelPanel'].arguments['scale']
        self.assertEqual(arg.name, 'scale')
        self.assertEqual(arg.type_, 'Number')

    def testConstructorMethodWithOneArgumentsWithDefaultValue(self):
        self.builder.addSource('''
        package com.gurufaction.asdox {
            import flash.net.*;
            public dynamic class ModelPanel extends Item {

                private var modelDesTA:TextArea;

                public function ModelPanel(scale:Number=0){
                }
            }
        }
        ''')
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["ModelPanel"]
        self.assertEqual(cls.name, 'ModelPanel')
        self.assertEqual(cls.visibility, 'public')
        self.assertEqual(cls.methods['ModelPanel'].name, 'ModelPanel')
        self.assertEqual(cls.methods['ModelPanel'].visibility, 'public')
        arg = cls.methods['ModelPanel'].arguments['scale']
        self.assertEqual(arg.name, 'scale')
        self.assertEqual(arg.type_, 'Number')

    def testConstructorMethodWithMultipleArguments(self):
        self.builder.addSource('''
        package com.gurufaction.asdox {
            import flash.net.*;
            public dynamic class ModelPanel extends Item {

                private var modelDesTA:TextArea;

                public function ModelPanel(
                    scale:Number,
                    modeltype:int,
                    addWidth:int,
                    addHeight:int){
                }
            }
        }
        ''')
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["ModelPanel"]
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["ModelPanel"]
        self.assertEqual(cls.name, 'ModelPanel')
        self.assertEqual(cls.visibility, 'public')
        self.assertEqual(cls.methods['ModelPanel'].name, 'ModelPanel')
        self.assertEqual(cls.methods['ModelPanel'].visibility, 'public')
        arg1 = cls.methods['ModelPanel'].arguments['scale']
        self.assertEqual(arg1.name, 'scale')
        self.assertEqual(arg1.type_, 'Number')
        arg2 = cls.methods['ModelPanel'].arguments['modeltype']
        self.assertEqual(arg2.name, 'modeltype')
        self.assertEqual(arg2.type_, 'int')
        arg3 = cls.methods['ModelPanel'].arguments['addWidth']
        self.assertEqual(arg3.name, 'addWidth')
        self.assertEqual(arg3.type_, 'int')
        arg4 = cls.methods['ModelPanel'].arguments['addHeight']
        self.assertEqual(arg4.name, 'addHeight')
        self.assertEqual(arg4.type_, 'int')

    def testConstructorMethodWithMultipleArgumentsWithDefaultValue(self):
        self.builder.addSource('''
        package com.gurufaction.asdox {
            import flash.net.*;
            public dynamic class ModelPanel extends Item {

                private var modelDesTA:TextArea;

                public function ModelPanel(
                    scale:Number = 4,
                    modeltype:int = 0,
                    addWidth:int =0 ,
                    addHeight:int = 0){
                }
            }
        }
        ''')
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["ModelPanel"]
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["ModelPanel"]
        self.assertEqual(cls.name, 'ModelPanel')
        self.assertEqual(cls.visibility, 'public')
        self.assertEqual(cls.methods['ModelPanel'].name, 'ModelPanel')
        self.assertEqual(cls.methods['ModelPanel'].visibility, 'public')
        arg1 = cls.methods['ModelPanel'].arguments['scale']
        self.assertEqual(arg1.name, 'scale')
        self.assertEqual(arg1.type_, 'Number')
        arg2 = cls.methods['ModelPanel'].arguments['modeltype']
        self.assertEqual(arg2.name, 'modeltype')
        self.assertEqual(arg2.type_, 'int')
        arg3 = cls.methods['ModelPanel'].arguments['addWidth']
        self.assertEqual(arg3.name, 'addWidth')
        self.assertEqual(arg3.type_, 'int')
        arg4 = cls.methods['ModelPanel'].arguments['addHeight']
        self.assertEqual(arg4.name, 'addHeight')
        self.assertEqual(arg4.type_, 'int')

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


    def testMethodStatic(self):
        self.builder.addSource('''
        package com.gurufaction.asdox
        {
            public class MyClass
            {
                public static function sayHi():String
                {
                }
            }
        }
        ''')
        pkg = self.builder.packages["com.gurufaction.asdox"]
        # from IPython import embed;embed();
        cls = pkg.classes["MyClass"]
        self.assertEqual(cls.methods["sayHi"].name, "sayHi")
        self.assertEqual(cls.methods["sayHi"].visibility, "public")
        self.assertEqual(cls.methods['sayHi'].isStatic, True)

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
        self.assertEqual(cls.methods["thanks"].type_, 'function')
        self.assertEqual(cls.methods['thanks'].return_type, 'String')
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
        m = cls.methods["addIntegers"]
        self.assertEqual(m.name, "addIntegers")
        self.assertEqual(m.type_, 'function')
        self.assertEqual(m.return_type, 'int')
        self.assertEqual(m.visibility, "public")
        self.assertEqual(m.isOverride, False)
        self.assertEqual(m.arguments["num1"].name, "num1")
        self.assertEqual(m.arguments["num1"].type_, "int")
        self.assertEqual(m.arguments["num2"].name, "num2")
        self.assertEqual(m.arguments["num2"].type_, "int")

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
        self.assertEqual(cls.methods["getName"].type_, 'function')
        self.assertEqual(cls.methods["getName"].return_type, 'String')
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
        self.assertEqual(cls.methods["getName"].type_, 'function')
        self.assertEqual(cls.methods["getName"].return_type, 'String')
        self.assertEqual(cls.methods["getName"].visibility, "public")
        self.assertEqual(cls.methods["getName"].isOverride, False)

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
        self.assertEqual(cls.methods["getName"].type_, 'function')
        self.assertEqual(cls.methods["getName"].return_type, 'String')
        self.assertEqual(cls.methods["getName"].visibility, "public")
        self.assertEqual(cls.methods["getName"].isOverride, False)
        self.assertEqual(
            cls.methods["getName"].metadata[0].name,
            "Bindable"
        )
        self.assertEqual(
            cls.methods["getName"].metadata[0].params,
            {0: 'dataChange'}
        )
        self.assertEqual(
            cls.methods["getName"].metadata[1].name,
            "Inspectable"
        )
        self.assertEqual(
            cls.methods["getName"].metadata[1].params,
            {'environment': 'none'}
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
        v = cls.variables["labelPlacement"]
        self.assertEqual(v.name, "labelPlacement")
        self.assertEqual(v.type_, "String")
        self.assertEqual(v.visibility, "public")
        self.assertEqual(v.readable, True)
        self.assertEqual(v.writable, False)
        self.assertEqual(v.isProperty, True)

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
        v = cls.variables["labelPlacement"]
        self.assertEqual(v.name, "labelPlacement")
        self.assertEqual(v.type_, "String")
        self.assertEqual(v.visibility, "public")
        self.assertEqual(v.readable, False)
        self.assertEqual(v.writable, True)
        self.assertEqual(v.isProperty, True)

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

                        dispatchEvent(
                            new FlexEvent(FlexEvent.VALUE_COMMIT)
                        );
                    }
                }
            }
        }
        """)
        pkg = self.builder.packages["com.gurufaction.asdox"]
        cls = pkg.classes["MyClass"]
        m = cls.methods["setSelected"]
        self.assertEqual(m.name, "setSelected")
        self.assertEqual(m.type_, 'function')
        self.assertEqual(m.return_type, 'void')
        self.assertEqual(m.visibility, "mx_internal")
        self.assertEqual(m.isOverride, False)
        self.assertEqual(
            cls.methods["setSelected"].arguments["value"].name,
            "value"
        )
        self.assertEqual(
            cls.methods["setSelected"].arguments["value"].type_,
            "Boolean"
        )
