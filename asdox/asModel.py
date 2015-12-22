#!/usr/bin/env python
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

class Documentable(object):
    "Actionscript Object that allows for JavaDoc declaration"
    pass

class Visible(object):
    def __init__(self):
        self.visibility = "internal"

class MetaTagable(object):
    "Actionscript Object that allows for MetaTags"
    def __init__(self):
        self.metadata = []

class ASType(object):
    "Actionscript 3 Type"

    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

    def __repr__(self):
        return '<ASType: {0}>'.format(self.name)

class ASVariable(ASType, Visible, MetaTagable):
    "Actionscript 3 Variable"

    def __init__(self, name='', type_='*'):
        ASType.__init__(self, name, type_)
        self.isStatic = False
        self.isConstant = False
        self.metadata = []
        self.readable = False
        self.writable = False
        self.isProperty = False

    def __repr__(self):
        return '<ASVariable: {0}>'.format(self.name)

class ASMetaTag(object):
    "Actionscript MetaTag Definition"

    def __init__(self, name=''):
        self.name = name
        self.params = {}

    def __repr__(self):
        return '<ASMetaTag: {0}>'.format(self.name)

class ASMethod(ASType, Visible, MetaTagable):
    "Actionscript Method Definition"

    def __init__(self, name='', type_='void'):
        self.isOverride = False
        self.isFinal = False
        self.isStatic = False
        self.name = name
        self.type_ = type_
        self.metadata = []
        self.arguments = {}

    def __repr__(self):
        return '<ASMethod: {0}>'.format(self.name)

class ASVirtualMethod(ASMethod):
    "Actionscript Virtual Method Definition"

    def __init__(self, name='', type_='void'):
        self.name = name
        self.type_ = type_
        self.metadata = []
        self.arguments = {}

    def __repr__(self):
        return '<ASVirtualMethod: {0}>'.format(self.name)

class ASClass(Visible,MetaTagable):
    "Actionscript Class Definition"

    def __init__(self, name = ''):
        self.name = name
        self.metadata = []
        self.variables = {}
        self.methods = {}
        self.extends = ''
        self.implements = []
        self.isDynamic = False
        self.isFinal = False
        self.isInterface = False

    def __repr__(self):
        return '<ASClass: {0}>'.format(self.name)

class ASPackage(Visible, MetaTagable):
    "Actionscript Package Definition"
    
    def __init__(self, name=''):
        self.name = name
        self.metadata = []
        self.classes = {}
        self.imports = []
        self.use_namespace = []

    def __repr__(self):
        return '<ASPackage: {0}>'.format(self.name)

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

