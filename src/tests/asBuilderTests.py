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
import unittest,sys,os
sys.path.append( os.path.abspath('../') )
from asdox import asModel,asBuilder

class BaseDefinitionTestCase(unittest.TestCase):
	def setUp(self):
		self.builder = asBuilder.Builder()
	def tearDown(self):
		pass
	def pkgTest(self,result,expected):
		self.assertEqual(result.__class__,expected.__class__)
		self.assertEqual(result.getName(),expected.getName())
		self.assertEqual(result.getType(),expected.getType())
		self.assertEqual(result.getImports(),expected.getImports())
	def clsTest(self,result,expected):
		self.assertEqual(result.__class__,expected.__class__)
		self.assertEqual(result.getName(),expected.getName())
		self.assertEqual(result.getType(),expected.getType())
		self.assertEqual(result.getModifiers(),expected.getModifiers())
		self.assertEqual(result.getIncludes(),expected.getIncludes())
		self.assertEqual(result.isInterface(),expected.isInterface())
	def metaTest(self,result,expected):
		self.assertEqual(result.getName(),expected.getName())
		self.assertEqual(result.getParams(),expected.getParams())
class ClassDefinitionTestCase(BaseDefinitionTestCase):
	def testClassMetaData(self):
		self.builder.addSource("""
		package test{
			[Bindable]
			[Event(name="myEnableEvent", type="flash.events.Event")]
			public class MyClass
			{
			}
		}
		""")
		# Test Package 'test'
		self.assertEqual(self.builder.hasPackage("test"),True,"Package 'test' not found.")
		pkg = self.builder.getPackage("test")
		self.assertEqual(pkg.getName(),"test","Package name not equal to 'test'.")
		self.assertEqual(pkg.getType(),"package","Package type not equal to 'package'.")
		# Test Class 'MyClass'
		self.assertEqual(pkg.hasClass("MyClass"),True,"Class 'MyClass' not found.")
		cls = pkg.getClass("MyClass")
		self.assertEqual(cls.isPublic(),True,"Class is not public")
		self.assertEqual(cls.getName(),"MyClass","Class name not equal to 'MyClass'.")
		self.assertEqual(cls.isDynamic(),False,"Class should not be dynamic.")
		self.assertEqual(cls.isFinal(),False,"Class should not be final.")
		self.assertEqual(len(cls.getFields()),0,"Class should contain no fields.")
		self.assertEqual(len(cls.getMethods()),0,"Class should contain no methods.")
		# Test MetaTags 'Bindable'
		self.assertEqual(cls.hasMetaTag("Bindable"),True,"MetaTag 'Bindable' not found.")
		meta = cls.getMetaTag("Bindable")
		self.assertEqual(meta.getName(),"Bindable","MetaTag name not equal to 'Bindable'.")
		self.assertEqual(meta.getType(),"metatag","MetaTag type not equal to 'metatag'.")
		self.assertEqual(len(meta.getParams()),0,"'Bindable' MetaTag should not contain any parameters.")
		# Test MetaTag 'Event'
		self.assertEqual(cls.hasMetaTag("Event"),True,"MetaTag 'Event' not found.")
		meta = cls.getMetaTag("Event")
		self.assertEqual(meta.getName(),"Event","MetaTag name not equal to 'Event'.")
		self.assertEqual(meta.getType(),"metatag","MetaTag type not equal to 'metatag'.")
		self.assertEqual(len(meta.getParams()),2,"'Event' MetaTag should contain 2 parameters.")
		self.assertEqual(meta.hasParam("name"),True,"'Event' MetaTag should have 'name' parameter.")
		self.assertEqual(meta.getParam("name"),"myEnableEvent","'name' parameter should equal 'myEnableEvent'.")
		self.assertEqual(meta.hasParam("type"),True,"'Event' MetaTag should have 'type' parameter.")
		self.assertEqual(meta.getParam("type"),"flash.events.Event","'type' parameter should equal 'flash.events.Event'.")
class PackageDefinitionTestCase(BaseDefinitionTestCase):
	
	def testDefaultPackage(self):
		self.builder.addSource("""
		package
		{
		}
		""")
		
		result = self.builder.getPackage("")
		#self.assertEqual(len(result),1)
		
		expected = asModel.ASPackage("");
		self.pkgTest(result,expected)
	def testPackage(self):
		self.builder.addSource("""
		package net.test.test
		{
		}
		""")
		
		result = self.builder.getPackage("net.test.test")
		#self.assertEqual(len(result),1)
		expected = asModel.ASPackage("net.test.test");
		self.pkgTest(result,expected)
	def testMultiPackages(self):
		self.builder.addSource("""
		package com.google.code.test
		{
		}
		
		package com.gurufaction.asDox
		{
		}
		
		package
		{
		}
		""")
		
		result = self.builder.getPackages()
		#self.assertEqual(len(result),3)
		
		expected = asModel.ASPackage("com.google.code.test");
		self.pkgTest(result["com.google.code.test"],expected)
		expected = asModel.ASPackage("com.gurufaction.asDox");
		self.pkgTest(result["com.gurufaction.asDox"],expected)
		expected = asModel.ASPackage("");
		self.pkgTest(result[""],expected)
	def testPackageWithClass(self):
		self.builder.addSource("""
		package com.gurufaction.mypackage
		{
			public class MyClass
			{
				include "file1.as"
				include "file2.as"
				public var test:String;
			}
		}
		""")
		
		result = self.builder.getPackage("com.gurufaction.mypackage")
		self.assertNotEqual( result,None)
		
		expected = asModel.ASPackage("com.gurufaction.mypackage");
		self.pkgTest(result,expected)
		
		cls = asModel.ASClass("MyClass");
		cls.addModifier("public")
		cls.addInclude("file1.as")
		cls.addInclude("file2.as")
		self.clsTest(result.getClass("MyClass"),cls)
if __name__ == "__main__":
	unittest.main()