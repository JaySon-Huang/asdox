#!/usr/bin/env
#encoding=utf-8

# Copyright (c) 2008, Michael Ramirez
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright notice, 
#     this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice, 
#     this list of conditions and the following disclaimer in the documentation 
#     and/or other #materials provided with the distribution.
#   * Neither the name of the <ORGANIZATION> nor the names of its contributors 
#     may be used to endorse or promote products derived from this software 
#     without specific #prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import unittest
sys.path.append( os.path.abspath('../') )
from asdox import asModel,asBuilder

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.builder = asBuilder.Builder()

    def tearDown(self):
        pass

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
        
        self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyBasicClass"].name,"MyBasicClass")
        self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyBasicClass"].visibility,"public")

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
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].visibility,"public")
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].metadata[0].name,"Event")
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].metadata[0].params,{'type': 'mx.events.FlexEvent', 'name': 'buttonDown'})

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
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].visibility,"public")
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].metadata[0].name,"DefaultTriggerEvent")
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].metadata[0].params,{0: 'click'})
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].metadata[1].name,"Event")
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].metadata[1].params,{'name': 'myEnableEvent','type':'flash.events.Event'})
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].metadata[2].name,"Bindable")
        self.assertEqual(self.builder.packages["test"].classes["MyClass"].metadata[2].params,{})

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
        self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyClass"].visibility,"public")

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
        self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyClass"].extends,"BaseClass")
        self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyClass"].visibility,"public")

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
        self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyClass"].implements[0],"IWorkable")
        self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyClass"].implements[1],"ITestable")

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
        self.assertEqual(self.builder.packages[""].classes["MyClass"].visibility,"internal")

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
        self.assertEqual(self.builder.packages[""].classes["MyClass"].visibility,"public")

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
        self.assertEqual(self.builder.packages[""].classes["MyClass"].isDynamic,True)

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
        self.assertEqual(self.builder.packages[""].classes["MyClass"].isFinal,True)

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
        self.assertEqual(self.builder.packages[""].classes["MyClass"].isDynamic,True)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].isFinal,True)

class ASPackageTestCase(BaseTestCase):
    
    def testUnnamedPackage(self):
        self.builder.addSource("""
        package
        {
            public class MyClass
                        {
                        
                        }
        }
        """)
        
        self.assertEqual(self.builder.packages[""].name,"")

    def testNamedPackage(self):
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            public class MyClass
                        {
                        
                        }
        }
        """)
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].name,"com.gurufaction.asdox")

    def testPackageImports(self):
        '''Parse Package with Import definitions.'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            import flash.display.DisplayObject;
            import flash.events.*;
            import flash.events.FocusEvent;
            import flash.events.KeyboardEvent;
            import flash.events.MouseEvent;
            import flash.events.TimerEvent;
            
            public class MyClass
                        {
                        
                        }
        }
        """)
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].imports,['flash.display.DisplayObject', 'flash.events', 'flash.events.FocusEvent', 'flash.events.KeyboardEvent', 'flash.events.MouseEvent', 'flash.events.TimerEvent'] )

    def testPackageSinglelineComments(self):
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            //--------------------------------------
            //  Events
            //--------------------------------------

            //--------------------------------------
            //  Styles
            //--------------------------------------
            public class MyClass
                        {
                        
                        }
        }
        """)
        
        self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)

    def testPackageMultilineComments(self):
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            /*
            *
            * Testing Multiline Comments
            * inside package definition.
            *
            */
            public class MyClass
                        {
                        
                        }
        }
        """)
        
        self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)

    def testPackageComments(self):
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            /*
            * First Multiline Comment
            */
            
            // First Singleline Comment
            
            /*
            * Second Multiline Comment
            */
            
            // Second Singleline Comment
            public class MyClass
                        {
                        
                        }
        }
        """)
        
        self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)

    def testPackageNamespace(self):
        '''Parse Package with namespace declaration.'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            use namespace mx_internal;
            public class MyClass
                        {
                        
                        }
        }
        """)
        
        self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)

    def testPackageIncludes(self):
        '''Parse Package with include statements.'''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            include "../styles/metadata/FocusStyles.as"
            include "../styles/metadata/LeadingStyle.as"
            include "../styles/metadata/PaddingStyles.as"
            include "../styles/metadata/SkinStyles.as"
            include "../styles/metadata/TextStyles.as"
            public class MyClass
                        {
                        
                        }
        }
        """)
        
        self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)

    def testSourceFileComment(self):
        '''Parse Package with leading comment.'''
        self.builder.addSource("""
        ////////////////////////////////////////////////////////////////////////////////
        //
        //  Copyright (C) 2003-2006 Adobe Macromedia Software LLC and its licensors.
        //  All Rights Reserved. The following is Source Code and is subject to all
        //  restrictions on such code as contained in the End User License Agreement
        //  accompanying this product.
        //
        ////////////////////////////////////////////////////////////////////////////////
        
        package com.gurufaction.asdox
        {
            public class MyClass
                        {
                        
                        }
        }
        """)
        
        self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)

class ParsingExternalFileTestCase(BaseTestCase):
    def testFilterClassFile(self):
        '''Load and Parse Filter.as source file.'''
        self.builder.addSource("resources/Filter.as")
        self.builder.addSource("resources/Filter2.as")
        self.assertEqual(self.builder.packages["com.franklinconnections"].imports,['mx.collections.ArrayCollection', 'mx.controls.Alert','com.foo2','com.foo3'])
        self.assertEqual(self.builder.packages["com.franklinconnections"].classes["Filter"].name,"Filter")

    def testButtonClassFile(self):
        '''Load and Parse Button.as source file.'''
        self.builder.addSource("resources/Button.as")
        self.assertEqual(self.builder.packages["mx.controls"].classes["Button"].name,"Button")

    def testUTF8ClassFile(self):
        '''Load and Parse UTF-8 source file.'''
        self.builder.addSource("resources/mx/utils/StringUtil.as")
        self.assertEqual(self.builder.packages["mx.utils"].classes["StringUtil"].name,"StringUtil")

class BuilderTestCase(BaseTestCase):        
    def testMultipleSources(self):
        '''Parse multiple source files.'''
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
        self.assertEqual(self.builder.packages["com.googlecode.asdox"].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages["com.googlecode.asdox"].classes["MyClass"].visibility,"internal")
        self.assertEqual(self.builder.packages["com.googlecode.asdox"].classes["MyOtherClass"].name,"MyOtherClass")
        self.assertEqual(self.builder.packages["com.googlecode.asdox"].classes["MyOtherClass"].visibility,"public")

    def testAddSourceDir(self):
        '''Parse directory for source files'''
        self.builder.addSource("resources/com/gurufaction")
        self.assertEqual(self.builder.packages["com.gurufaction"].classes["MyClassFile1"].name,"MyClassFile1")
        self.assertEqual(self.builder.packages["com.gurufaction"].classes["MyClassFile1"].visibility,"internal")
        self.assertEqual(self.builder.packages["com.gurufaction"].classes["MyClassFile2"].name,"MyClassFile2")
        self.assertEqual(self.builder.packages["com.gurufaction"].classes["MyClassFile2"].visibility,"internal")


class ASFieldTestCase(BaseTestCase):
    def testClassField(self):
        '''Parse class field.'''
        self.builder.addSource(""" 
        package 
        {
            class MyClass
            {
                internal var today:DateTime;
            }
        }
        """)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["today"].name,"today")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["today"].type,"DateTime")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["today"].visibility,"internal")

    def testConstantClassField(self):
        '''Parse class constant field.'''
        self.builder.addSource(""" 
        package 
        {
            class MyClass
            {
                internal const PI:Number;
            }
        }
        """)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["PI"].name,"PI")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["PI"].type,"Number")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["PI"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["PI"].isConstant,True)

    def testStaticClassField(self):
        '''Parse class static field.'''
        self.builder.addSource(""" 
        package 
        {
            class MyClass
            {
                internal static var count:int;
            }
        }
        """)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["count"].name,"count")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["count"].type,"int")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["count"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["count"].isConstant,False)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["count"].isStatic,True)

    def testFieldModifiers(self):
        '''Parse field modifiers'''
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
        self.assertEqual(self.builder.packages[""].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].name,"name")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].type,"String")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].visibility,"public")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].isConstant,False)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["age"].name,"age")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["age"].type,"int")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["age"].visibility,"private")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["age"].isConstant,False)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["salary"].name,"salary")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["salary"].type,"Number")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["salary"].visibility,"protected")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["salary"].isConstant,False)

    def testFieldInitialization(self):
        '''Parse field initialization'''
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
        self.assertEqual(self.builder.packages[""].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].name,"name")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].type,"String")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].isConstant,False)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["age"].name,"age")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["age"].type,"int")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["age"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["age"].isConstant,False)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["salary"].name,"salary")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["salary"].type,"Number")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["salary"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["salary"].isConstant,False)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["isSmart"].name,"isSmart")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["isSmart"].type,"Boolean")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["isSmart"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["isSmart"].isConstant,False)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["_labelPlacement"].name,"_labelPlacement")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["_labelPlacement"].type,"String")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["_labelPlacement"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["_labelPlacement"].isConstant,False)

    def testFieldNamespaceModifier(self):
        '''Parse class namespace modifier'''
        self.builder.addSource(""" 
        package
        {
                class MyClass
            { 
                mx_internal var name:String;
            }
        }
        """)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].name,"name")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].type,"String")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].visibility,"mx_internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].isConstant,False)   

    def testMetaDataWithClassFields(self):
        '''Parse class Fields with metadata'''
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
        self.assertEqual(self.builder.packages[""].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].visibility,"internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].name,"name")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].type,"String")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].visibility,"mx_internal")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].isConstant,False)
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].metadata[0].name,"Bindable")
        self.assertEqual(self.builder.packages[""].classes["MyClass"].variables["name"].metadata[0].params,{})


class ASMethodTestCase(BaseTestCase):
    "Test cases for class methods"
    def testConstructorMethod(self):
        '''Parse class constructor method with no arguments.'''
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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].visibility,"public")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["MyClass"].name,"MyClass")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["MyClass"].visibility,"public")

    def testMethod(self):
        '''Parse class method with no arguments.'''
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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["sayHi"].name,"sayHi")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["sayHi"].visibility,"public")

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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["thanks"].name,"thanks")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["thanks"].type,"String")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["thanks"].visibility,"public")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["thanks"].isOverride,True)

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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["addIntegers"].name,"addIntegers")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["addIntegers"].type,"int")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["addIntegers"].visibility,"public")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["addIntegers"].isOverride,False)
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["addIntegers"].arguments["num1"].name,"num1")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["addIntegers"].arguments["num1"].type,"int")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["addIntegers"].arguments["num2"].name,"num2")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["addIntegers"].arguments["num2"].type,"int")

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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].name,"getName")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].type,"String")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].visibility,"public")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].isOverride,False)

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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].name,"getName")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].type,"String")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].visibility,"public")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].isOverride,False)

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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].name,"getName")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].type,"String")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].visibility,"public")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].isOverride,False)
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].metadata[0].name,"Inspectable")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].metadata[0].params,{'environment': 'none'})
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].metadata[1].name,"Bindable")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["getName"].metadata[1].params,{0: 'dataChange'})

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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].name,"labelPlacement")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].type,"String")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].visibility,"public")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].readable,True)
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].writable,False)
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].isProperty,True)

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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].name,"labelPlacement")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].type,"String")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].visibility,"public")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].readable,False)
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].writable,True)
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["labelPlacement"].isProperty,True)

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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["name"].name,"name")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["name"].type,"String")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["name"].visibility,"public")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["name"].readable,True)
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["name"].writable,True)
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].variables["name"].isProperty,True)

    def testMethodNamespace(self):
        '''Parse class method with namespace.'''
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
        
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["setSelected"].name,"setSelected")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["setSelected"].type,"void")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["setSelected"].visibility,"mx_internal")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["setSelected"].isOverride,False)
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["setSelected"].arguments["value"].name,"value")
        self.assertEqual(self.builder.packages["com.gurufaction.asdox"].classes["MyClass"].methods["setSelected"].arguments["value"].type,"Boolean")


if __name__ == "__main__":
    unittest.main()
