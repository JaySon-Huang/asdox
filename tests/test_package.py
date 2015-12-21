#!/usr/bin/env python
#encoding=utf-8

import unittest
from helper import BaseTestCase

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
        pkg = self.builder.packages["com.gurufaction.asdox"]
        self.assertEqual(pkg.name, "com.gurufaction.asdox")

    def testPackageImports(self):
        '''
        Parse Package with Import definitions.
        '''
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
        pkg = self.builder.packages["com.gurufaction.asdox"]
        self.assertEqual(
            pkg.imports,
            ['flash.display.DisplayObject',
            'flash.events.*',
            'flash.events.FocusEvent',
            'flash.events.KeyboardEvent',
            'flash.events.MouseEvent',
            'flash.events.TimerEvent']
        )

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
        
        self.assertEqual(
            "com.gurufaction.asdox" in self.builder.packages,
            True
        )

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
        self.assertEqual(
            "com.gurufaction.asdox" in self.builder.packages,
            True
        )

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
        self.assertEqual(
            "com.gurufaction.asdox" in self.builder.packages,
            True
        )

    def testPackageNamespace(self):
        '''
        Parse Package with namespace declaration.
        '''
        self.builder.addSource("""
        package com.gurufaction.asdox
        {
            use namespace mx_internal;
            public class MyClass
            {
            }
        }
        """)
        self.assertEqual(
            "com.gurufaction.asdox" in self.builder.packages,
            True
        )

    @unittest.skip("FIXME: imclude statements")
    def testPackageIncludes(self):
        '''
        Parse Package with include statements.
        '''
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
        
        self.assertEqual(
            "com.gurufaction.asdox" in self.builder.packages,
            True
        )

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
        
        self.assertEqual(
            "com.gurufaction.asdox" in self.builder.packages,
            True
        )
