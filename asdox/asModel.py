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
class Documentable:
	"Actionscript Object that allows for JavaDoc declaration"
	pass
class Visible:
	visibility = "internal"
	def __init__(self):
		self.visibility = "internal"
class MetaTagable:
	"Actionscript Object that allows for MetaTags"
	metadata = []
class ASType:
	"Actionscript 3 Type"
	name = "";
	type = "";
	def __init__(self,name,type):
		self.name = name
		self.type = type
class ASVariable(ASType,Visible,MetaTagable):
	"Actionscript 3 Variable"
	isStatic = False
	isConstant = False
	readable = False
	writable = False
	isProperty = False
	def __init__(self, name = "", type = "*"):
		ASType.__init__(self,name,type)
		self.metadata = []
		self.readable = False
		self.writable = False
		self.isProperty = False
class ASMetaTag:
	"Actionscript MetaTag Definition"
	params = dict()
	name = ""
	def __init__(self,name = ""):
		self.name = name
		self.params = dict()
class ASClass(Visible,MetaTagable):
	"Actionscript Class Definition"
	name = ""
	variables = dict()
	methods = dict()
	extends = ""
	implements = []
	isDynamic = False
	isFinal = False
	isInterface = False
	def __init__(self, name = ""):
		self.name = name
		self.metadata = []
		self.variables = dict()
		self.methods = dict()
		self.extends = ""
		self.implements = []
		self.isDynamic = False
		self.isFinal = False
		self.isInterface = False
class ASPackage(Visible,MetaTagable):
	"Actionscript Package Definition"
	classes = dict()
	imports = []
	def __init__(self, name = ""):
		self.name = name
		self.metadata = []
		self.classes = dict()
		self.imports = []
	def toString(self):
		print "Package: " + self.name
		for cls in self.classes.values():
			print cls.visibility + " class " + cls.name + " implements " + str(cls.implements)
			for meta in cls.metadata:
				print "\t\t[" + meta.name + "]"
			for meth in cls.methods.values():
				for meta in meth.metadata:
					print "\t\t[" + meta.name + "]"
				print "\t\tMethod: " + meth.visibility + " " + meth.name + ":" + meth.type
				for arg in meth.arguments.values():
					print "\t\t\tArguments: " + arg.name + ":" + arg.type
			for var in cls.variables.values():
				for meta in var.metadata:
					print "\t\t[" + meta.name + "]"
				print "\t\tVariables: " + var.visibility + " " + var.name + ":" + var.type
			for prop in cls.properties.values():
				for meta in prop.metadata:
					print "\t\t[" + meta.name + "]"
				print "\t\tProperty: " + prop.visibility + " " + prop.name + ":" + prop.type	
class ASMethod(ASType,Visible,MetaTagable):
	"Actionscript Method Definition"
	arguments = dict()
	isOverride = False
	isFinal = False
	isStatic = False
	def __init__(self, name = "", type = "void"):
		self.name = name
		self.type = type
		self.metadata = []
		self.arguments = dict()
	