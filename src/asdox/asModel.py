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
class Includable:
	includes = set()
	def addInclude(self,inc):
		includes.add(inc)
	def getIncludes(self):
		return includes
	def hasInclude(self,inc):
		return inc in includes
class Documentable:
	pass
class Modifiable:
	modifiers = set()
	ACCESS_MODIFIERS = set()
	TYPE_MODIFIERS =  set()
	def addModifier(self, mod):
		self.modifiers = self.modifiers.union( self.ACCESS_MODIFIERS.union(self.TYPE_MODIFIERS).intersection(set([mod])) )
		if mod in self.ACCESS_MODIFIERS:
			self.modifiers.difference_update( self.ACCESS_MODIFIERS.difference(set([mod])))
	def hasModifier(self,mod):
		return mod in self.modifiers
	def getModifiers(self):
		return self.modifiers
class Typeable:
	"Actionscript Type Definition"
	name = ""
	type = ""
	def __init__(self,name,type):
		self.name = name
		self.type = type
class MetaTagable:
	metadata = dict()
	def addMetadata(self,meta):
		self.metadata[meta.name] = meta
	def getMetadata(self,name):
		return self.metadata[name]
class ASMetaTage(Typeable):
	"Actionscript MetaTag Definition"
	attributes = dict()
	def __init__(self,name = "",type = "metatag"):
		self.name = name
		self.type = type
class ASPackage(Typeable,Includable):
	"Actionscript Package Definition"
	def __init__(self,name = "",type = "package"):
		self.name = name;
		self.type = type;
	__classes = dict()
	imports = set()
	def addClass(self,cls):
		self.__classes[cls.name] = cls
	def getClass(self,name):
		return self.__classes[name]
	def getClasses(self):
		return self.__classes.values
class ASClass(Typeable,Modifiable,MetaTagable,Documentable,Includable):
	"Actionscript Class Definition"
	__fields = dict()
	__methods = dict()
	extends = "Object"
	implements = set()
	modifiers = set()
	ACCESS_MODIFIERS = set(['public','internal'])
	TYPE_MODIFIERS =  set(['final','dynamic'])
	def __init__(self,name = "",type = "class"):
		self.name = name;
		self.type = type;
		self.modifiers.add("internal")
	def addField(self,field):
		self.__fields[field.name] = field
	def getField(self,name):
		return self.__fields[name]
	def getField(self):
		return self.__fields.values
	def addMethod(self,method):
		self.__methods[method.name] = method
	def getMethod(self,name):
		return self.__methods[name]
	def getMethods(self):
		return self.__methods.values
	def isDynamic(self):
		return self.hasModifier("dynamic")
	def isFinal(self):
		return self.hasModifier("final")
	def isPublic(self):
		return self.hasModifier("public")
	def isInterface(self):
		return self.type == "interface"

class ASField(Typeable,Modifiable,MetaTagable,Documentable):
	"Actionscript Field Definition"
	__isConst = False
	modifiers = set()
	ACCESS_MODIFIERS = set(['public','internal','private','protected'])
	TYPE_MODIFIERS =  set(['static'])
	def __init__(self, name = "", type = "*"):
		self.name = name
		self.type = type
		self.modifiers.add("internal")
	def isStatic(self):
		return self.hasModifer("static")
	def isConstant(self):
		return self.__isConst
	
class ASMethod(Typeable,Modifiable,MetaTagable,Documentable):
	"Actionscript Method Definition"
	modifiers = set()
	ACCESS_MODIFIERS = set(['public','internal','private','protected'])
	TYPE_MODIFIERS =  set(['final','override','static'])
	def __init__(self, name = "", type = "void"):
		self.name = name
		self.type = type
	arguments = list()