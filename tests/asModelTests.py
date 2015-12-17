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
from asdox import asModel

class ASClassTestCase(unittest.TestCase):
	def testClassContructor(self):
		cls = asModel.ASClass();
		self.assertEqual(cls.name,"")
		cls = asModel.ASClass("ITestable")
		self.assertEqual(cls.name,"ITestable")
	def testBasicClass(self):
		cls = asModel.ASClass("MyClass")
		self.assertEqual(cls.name,"MyClass")
		self.assertEqual(cls.isInterface,False)
		self.assertEqual(cls.isDynamic,False)
		self.assertEqual(cls.isFinal,False)
		self.assertEqual(cls.visibility,"internal")
		self.assertEqual(cls.extends,"")
		self.assertEqual(cls.implements,[])
	def testClassVariables(self):
		cls = asModel.ASClass("VariableClass")
		var1 = asModel.ASVariable("name","String")
		var2 = asModel.ASVariable("age","int")
		var1.visibility = "private"
		var2.visibility = "public"
		cls.variables[var1.name] = var1
		cls.variables[var2.name] = var2
		self.assertEqual(cls.name,"VariableClass")
		self.assertEqual(cls.variables["name"].name,"name")
		self.assertEqual(cls.variables["name"].type,"String")
		self.assertEqual(cls.variables["name"].visibility,"private")
		self.assertEqual(cls.variables["age"].name,"age")
		self.assertEqual(cls.variables["age"].type,"int")
		self.assertEqual(cls.variables["age"].visibility,"public")
	def testClassMethods(self):
		cls = asModel.ASClass("MethodClass")
		meth1 = asModel.ASMethod("SayHello","String")
		meth2 = asModel.ASMethod("DoNothing")
		cls.methods[meth1.name] = meth1
		cls.methods[meth2.name] = meth2
		self.assertEqual(cls.name,"MethodClass")
		self.assertEqual( cls.methods["SayHello"].name,"SayHello")
		self.assertEqual( cls.methods["SayHello"].type,"String")
		self.assertEqual( cls.methods["DoNothing"].name,"DoNothing")
		self.assertEqual( cls.methods["DoNothing"].type,"void")
	def testBasicInterface(self):
		cls = asModel.ASClass("com.gurufaction.TestClass")
		cls.isInterface = True
		self.assertEqual(cls.name,"com.gurufaction.TestClass")
		self.assertEqual(cls.isInterface,True,"isInterface() method failed")
		self.assertEqual(cls.isDynamic,False)
		self.assertEqual(cls.isFinal,False)
		self.assertEqual(cls.visibility,"internal")
		self.assertEqual(cls.extends,"")
		self.assertEqual(cls.implements,[])
	def testClassModifiers(self):
		cls = asModel.ASClass()
		cls.visibility = "public"
		cls.isDynamic = True
		cls.isFinal = True
		self.assertEqual(cls.visibility,"public")
		self.assertEqual(cls.isDynamic,True)
		self.assertEqual(cls.isFinal,True)
if __name__ == "__main__":
	unittest.main()