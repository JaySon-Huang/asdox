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
from pyparsing import *
import os,fnmatch
from asModel import *

stack = []
metatags = []
imports = []
package = ASPackage()
class_name = ""
def parseASPackage( s,l,t ):
    global imports,package
    package.name = t.name
def parseASClass( s,l,t):
    global class_name
    cls = ASClass(t.name)
    cls.extends = t.extends
    if len(t.implements) > 0 :
	cls.implements = t.implements[0]
    if t.visibility == "":
	cls.visibility = "internal"
    else:
	cls.visibility = t.visibility
    if t.dynamic == "dynamic":
	cls.isDynamic = True
    if t.final == "final":
	cls.isFinal = True
    while metatags:
	tag= metatags.pop()
	cls.metadata.append(tag)
    class_name = cls.name
    package.classes[cls.name] = cls
def parseASArg(s,l,t):
    arg = ASType(t.name,t.type)
    return arg
def parseImports(s,l,t):
    global imports
    package.imports.append(t.name)
def parseASMetaTag(s,l,t):
    global metatags
    meta = ASMetaTag(t.name)
    index = 0
    for att in t.attributes:
	if att.key == "":
	    meta.params[index] = att.value
	else:
	    meta.params[att.key] = att.value
	index = index + 1
    metatags.append(meta)
def parseJavaDoc(s,l,t):
    pass
def parseASMethod(s,l,t):
    global class_name,package,metatags
    meth = ASMethod(t.name,t.type)
    meth.visibility = t.visibility
    if t.override:
	meth.isOverride = True
    if t.final:
	meth.isFinal = True
    if t.static:
	meth.isStatic = True
    for args in t.arguments:
	for arg in args:
	    meth.arguments[arg.name] =  arg
    if t.accessor:
	if package.classes[class_name].variables.has_key(meth.name) == False:
	    package.classes[class_name].variables[meth.name] = ASVariable(meth.name,meth.type)
	
	if t.accessor == "get":
	    package.classes[class_name].variables[meth.name].readable = True
	    package.classes[class_name].variables[meth.name].type = meth.type
	if t.accessor == "set":
	    package.classes[class_name].variables[meth.name].writable = True
	    for arg in meth.arguments.values():
		package.classes[class_name].variables[meth.name].type = arg.type
	while metatags:
	    tag = metatags.pop()
	    package.classes[class_name].variables[meth.name].metadata.append(tag)
	package.classes[class_name].variables[meth.name].visibility = t.visibility
	package.classes[class_name].variables[meth.name].isProperty = True
	if t.override:
	    package.classes[class_name].variables[meth.name].isOverride = True
	if t.final:
	    package.classes[class_name].variables[meth.name].isFinal = True
	if t.static:
	    package.classes[class_name].variables[meth.name].isStatic = True
    else:
	package.classes[class_name].methods[meth.name] = meth
	while metatags:
	    tag = metatags.pop()
	    package.classes[class_name].methods[meth.name].metadata.append(tag)
def parseASVariable(s,l,t):
    global metatags,class_name,package
    var = ASVariable(t.name,t.type)
    if t.kind == "const":
	var.isConstant = True
    if t.visibility == "":
	var.visibility = "internal"
    else:
	var.visibility = t.visibility
    if t.static == "static":
	var.isStatic = True
    package.classes[class_name].variables[var.name] = var
    package.classes[class_name].variables[var.name].readable = True
    package.classes[class_name].variables[var.name].writable = True
    while metatags:
	tag= metatags.pop()
	package.classes[class_name].variables[var.name].metadata.append(tag)
def locate(pattern, root=os.getcwd()):
		for path, dirs, files in os.walk(root):
			for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
				yield filename
COMMA,COLON,LPARN,RPARN,LCURL,RCURL,EQUAL,SEMI,LSQUARE,RSQUARE = map(Suppress,",:(){}=;[]")

PACKAGE = Keyword("package")
CLASS = Keyword("class")
IMPLEMENTS = Keyword("implements").suppress()
EXTENDS = Keyword("extends").suppress()
FUNCTION = Keyword("function").suppress()
IMPORT = Keyword("import").suppress()
INCLUDE = Keyword("include").suppress()
INTERFACE = Keyword("interface")
INTERNAL = Keyword("internal")
PUBLIC = Keyword("public")
PRIVATE = Keyword("private")
PROTECTED = Keyword("protected")
MXINTERNAL = Keyword("mx_internal")
STATIC = Keyword("static")
PROTOTYPE = Keyword("prototype")
FINAL = Keyword("final")
OVERRIDE = Keyword("override")
NATIVE = Keyword("native")
DYNAMIC = Keyword("dynamic")
USE = Keyword("use")
NAMESPACE = Keyword("namespace")
VAR = Keyword("var")
CONST = Keyword("const")
GET = Keyword("get")
SET = Keyword("set")
DOT = "."
STAR = "*"
REST = "..."
UNDERSCORE = "_"
TERMINATOR = Optional(SEMI)

point = Literal('.')
e = CaselessLiteral('E')
plusorminus = Literal('+') | Literal('-')
number = Word(nums) 
integer = Combine( Optional(plusorminus) + number )
floatnumber = Combine( integer + Optional( point + Optional(number) ) + Optional( e + integer ) )
HEX = "0x" + Word(hexnums)

########################## NEW GRAMMAR DEFINITION ##############################
IDENTIFIER = Word(alphas + '_',alphanums + '_') 
QUALIFIED_IDENTIFIER = Combine(IDENTIFIER + ZeroOrMore( DOT + IDENTIFIER ))
SINGLE_LINE_COMMENT = dblSlashComment
MULTI_LINE_COMMENT = cStyleComment
JAVADOC_COMMENT = (Regex(r"/\*\*(?:[^*]*\*+)+?/")).setParseAction(parseJavaDoc)
COMMENTS = SINGLE_LINE_COMMENT.suppress() ^ JAVADOC_COMMENT ^ MULTI_LINE_COMMENT.suppress()
DBL_QUOTED_STRING = QuotedString(quoteChar="\"", escChar='\\')
SINGLE_QUOTED_STRING = QuotedString(quoteChar="'", escChar='\\')
ARRAY_INIT = LSQUARE + RSQUARE
VALUE = floatnumber ^ QUALIFIED_IDENTIFIER ^ DBL_QUOTED_STRING ^ SINGLE_QUOTED_STRING ^ integer ^ HEX
INIT = QuotedString(quoteChar="=", endQuoteChar=";",multiline="true") ^ (EQUAL + DBL_QUOTED_STRING + TERMINATOR)
TYPE = COLON + (QUALIFIED_IDENTIFIER ^ STAR)("type")
VARIABLE_MODIFIERS = Optional(STATIC("static")) & Optional(IDENTIFIER("visibility"))
VARIABLE_DEFINITION = ( VARIABLE_MODIFIERS + (CONST ^ VAR)("kind") + IDENTIFIER("name")  + Optional(TYPE) + Optional(MULTI_LINE_COMMENT) + (INIT ^ TERMINATOR)).setParseAction(parseASVariable)
USE_NAMESPACE = USE + NAMESPACE + QUALIFIED_IDENTIFIER + TERMINATOR
ATTRIBUTES =  (Optional(IDENTIFIER("key") + EQUAL) + VALUE("value") ).setResultsName("attributes",listAllMatches="true")
METATAG = (LSQUARE + IDENTIFIER("name") + Optional( LPARN + delimitedList(ATTRIBUTES) + RPARN ) + RSQUARE).setParseAction(parseASMetaTag)
INCLUDE_DEFINITION = INCLUDE + QuotedString(quoteChar="\"", escChar='\\') + TERMINATOR
IMPORT_DEFINITION = (IMPORT + QUALIFIED_IDENTIFIER("name") + Optional(DOT + STAR) + TERMINATOR).setParseAction(parseImports)
BLOCK = Suppress( nestedExpr("{","}") )
BASE_BLOCK = USE_NAMESPACE ^ COMMENTS ^ METATAG ^ INCLUDE_DEFINITION
METHOD_MODIFIER = Optional(STATIC("static")) & ( Optional(OVERRIDE("override")) & Optional(FINAL("final")) & Optional(IDENTIFIER("visibility")) )
METHOD_PARAMETERS = IDENTIFIER("name") + TYPE + (Optional( EQUAL + VALUE ) & Optional(MULTI_LINE_COMMENT) )
METHOD_SIGNATURE = FUNCTION + Optional(GET ^ SET)("accessor") + IDENTIFIER("name") + LPARN + Optional(delimitedList(METHOD_PARAMETERS.setParseAction(parseASArg)).setResultsName("arguments",listAllMatches="true")) + Optional( Optional(COMMA) + REST + IDENTIFIER) + RPARN + Optional( TYPE ) + Optional(COMMENTS)
METHOD_DEFINITION = (METHOD_MODIFIER + METHOD_SIGNATURE  + BLOCK).setParseAction(parseASMethod)
CLASS_IMPLEMENTS = IMPLEMENTS + delimitedList( QUALIFIED_IDENTIFIER ).setResultsName("implements",listAllMatches="true")
CLASS_BLOCK = LCURL + ZeroOrMore( IMPORT_DEFINITION ^ BASE_BLOCK ^ VARIABLE_DEFINITION ^ METHOD_DEFINITION ) + RCURL
CLASS_EXTENDS = EXTENDS + QUALIFIED_IDENTIFIER("extends")
INTERFACE_EXTENDS = EXTENDS + delimitedList( QUALIFIED_IDENTIFIER )
BASE_MODIFIERS = INTERNAL ^ PUBLIC
CLASS_MODIFIERS = Optional(FINAL("final")) & Optional(DYNAMIC("dynamic")) & Optional(BASE_MODIFIERS("visibility"))
CLASS_DEFINITION = (CLASS_MODIFIERS + CLASS + QUALIFIED_IDENTIFIER("name") + Optional( CLASS_EXTENDS ) + Optional( CLASS_IMPLEMENTS ) ).setParseAction(parseASClass) + CLASS_BLOCK 
INTERFACE_BLOCK = LCURL + ZeroOrMore( IMPORT_DEFINITION ^ BASE_BLOCK ^ VARIABLE_DEFINITION ^ (METHOD_SIGNATURE + TERMINATOR) ) + RCURL
INTERFACE_DEFINITION = Optional(BASE_MODIFIERS) + INTERFACE + QUALIFIED_IDENTIFIER + Optional( INTERFACE_EXTENDS ) + INTERFACE_BLOCK
PACKAGE_BLOCK = LCURL + ZeroOrMore( IMPORT_DEFINITION ^ BASE_BLOCK ) + (CLASS_DEFINITION ^ INTERFACE_DEFINITION) + RCURL
PACKAGE_DEFINITION = (PACKAGE + Optional( QUALIFIED_IDENTIFIER("name") ) ).setParseAction(parseASPackage) + PACKAGE_BLOCK 
# Windows 下文件的 BOM 头
BOM = Literal('\xEF\xBB\xBF').suppress()
PROGRAM = (
    Optional(BOM)
    + ZeroOrMore(COMMENTS)
    + PACKAGE_DEFINITION
)
