#!/usr/bin/env python
# encoding=utf-8

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
from pyparsing import *
from asModel import *

# _isTracing = True
_isTracing = False

def parseASPackage(s, location, tokens):
    # from IPython import embed;embed();
    if _isTracing:
        print('parseASPackage[{0}] @ loc({1})'.format(tokens.name, location))
    pkg = ASPackage()
    pkg.name = tokens.name
    if tokens.imports:
        pkg.imports += tokens.imports.asList()
    if tokens.use_namespace:
        pkg.use_namespace += tokens.use_namespace.asList()
    # 定义的类
    if tokens.class_:
        cls = tokens.class_[0]
        pkg.classes[cls.name] = cls
    # 定义的接口
    if tokens.interface:
        cls = tokens.interface[0]
        pkg.classes[cls.name] = cls
    return pkg

def parseASClass(s, location, tokens):
    if _isTracing:
        print('parseASClass[{0}] @ loc({1})'.format(tokens.name, location))
    cls = ASClass(tokens.name)
    # 基类 & 接口
    cls.extends = tokens.extends
    if tokens.implements:
        cls.implements = tokens.implements.asList()
    # 可见性
    if tokens.visibility == '':
        cls.visibility = 'internal'
    else:
        cls.visibility = tokens.visibility
    # 其他属性
    if tokens.dynamic == 'dynamic':
        cls.isDynamic = True
    if tokens.final == 'final':
        cls.isFinal = True
    # metatag
    if tokens.metatag:
        cls.metadata.append(tokens.metatag[0])
    for variable in tokens.variables:
        variable = variable[0]
        cls.variables[variable.name] = variable
    # methods
    for method in tokens.methods:
        method = method[0]
        cls.methods[method.name] = method
        # TODO: getter/setter 对相关变量属性进行设置
    # from IPython import embed;embed();
    return ParseResults(cls)

def parseImports(s, location, tokens):
    if _isTracing:
        print('parseImports[{0}] @ loc({1})'.format(tokens.name, location))
    return tokens.name

def parseASMetaTag(s, location, tokens):
    if _isTracing:
        print('parseASMetaTag[{0}] @ loc({1})'.format(tokens.name, location))
    metatag = ASMetaTag(tokens.name)
    index = 0
    for attr in tokens.attributes:
        if attr.key == '':
            metatag.params[index] = attr.value
        else:
            metatag.params[attr.key] = attr.value
        index = index + 1
    return ParseResults(metatag)

def parseJavaDoc(s, location, tokens):
    pass

def parseASArg(s, location, tokens):
    if _isTracing:
        print('parseASArg[{0}] @ loc({1})'.format(tokens.name, location))
        # from IPython import embed;embed();
    arg = ASType(tokens.name, tokens.type_)
    return arg

def parseASMethod(s, location, tokens):
    if _isTracing:
        print('[method BEGIN] {0}'.format(tokens.name))
    # 返回类型
    if tokens.type_:
        method = ASMethod(tokens.name, tokens.type_)
    else:
        method = ASMethod(tokens.name)
    # 可见域
    if tokens.visibility:
        method.visibility = tokens.visibility
    else:
        method.visibility = 'internal'
    # method 属性
    if tokens.override:
        method.isOverride = True
    if tokens.final:
        method.isFinal = True
    if tokens.static:
        method.isStatic = True
    # method 传入参数
    for arg in tokens.arguments:
        method.arguments[arg.name] = arg
    # from IPython import embed;embed();
    if _isTracing:
        print('[method END] {0}'.format(repr(method)))
    return ParseResults(method)

def parseASVariable(s, location, tokens):
    if _isTracing:
        print('parseASVariable[{0}] @ loc({1})'.format(tokens.name, location))
    var = ASVariable(tokens.name, tokens.type_)
    if tokens.visibility == '':
        var.visibility = 'internal'
    else:
        var.visibility = tokens.visibility
    # 静态量
    if tokens.static == 'static':
        var.isStatic = True
    # 常量/变量
    if tokens.kind == 'const':
        var.isConstant = True
        var.readable = True
        var.writable = False
    else:
        var.readable = True
        var.writable = True
    # from IPython import embed;embed();
    return ParseResults(var)

def debug(s, location, tokens):
    from IPython import embed;embed();


KEYWORDS = {}
KEYWORDS['package'] = Keyword('package')
KEYWORDS['class'] = Keyword('class')
KEYWORDS['implements'] = Keyword('implements').suppress()
KEYWORDS['extends'] = Keyword('extends').suppress()
KEYWORDS['function'] = Keyword('function').suppress()
KEYWORDS['import'] = Keyword('import').suppress()
KEYWORDS['include'] = Keyword('include').suppress()
KEYWORDS['interface'] = Keyword('interface')

KEYWORDS['internal'] = Keyword('internal')
KEYWORDS['public'] = Keyword('public')
KEYWORDS['private'] = Keyword('private')
KEYWORDS['private'] = Keyword('private')
KEYWORDS['protected'] = Keyword('protected')
KEYWORDS['mxinternal'] = Keyword('mx_internal')

KEYWORDS['static'] = Keyword('static')
KEYWORDS['prototype'] = Keyword('prototype')
KEYWORDS['final'] = Keyword('final')
KEYWORDS['override'] = Keyword('override')
KEYWORDS['native'] = Keyword('native')
KEYWORDS['dynamic'] = Keyword('dynamic')

KEYWORDS['use'] = Keyword('use')
KEYWORDS['namespace'] = Keyword('namespace')

KEYWORDS['var'] = Keyword('var')
KEYWORDS['const'] = Keyword('const')

KEYWORDS['get'] = Keyword('get')
KEYWORDS['set'] = Keyword('set')

COMMA,COLON,SEMI,EQUAL = list(map(Suppress, ',:;='))
LPARN,RPARN,LCURL,RCURL,LSQUARE,RSQUARE = list(map(Suppress,'(){}[]'))
UNDERSCORE = Literal('_')
STAR = Literal('*')
DOT = Literal('.')
REST = Literal('...')
TERMINATOR = Optional(SEMI)

# 数字
point = Literal('.')
e = CaselessLiteral('E')
plusOrMinus = Literal('+') | Literal('-')
number = Word(nums)
integer = Combine(Optional(plusOrMinus) + number)
floatnumber = Combine(
    integer
    + Optional(point + Optional(number))
    + Optional( e + integer )
)
HEX = '0x' + Word(hexnums)

########################## NEW GRAMMAR DEFINITION ###########################
# 标识符
IDENTIFIER = Word(alphas+'_', alphanums+'_') 
QUALIFIED_IDENTIFIER = Combine(IDENTIFIER + ZeroOrMore(DOT + IDENTIFIER))
# 注释相关
SINGLE_LINE_COMMENT = dblSlashComment
MULTI_LINE_COMMENT = cStyleComment
JAVADOC_COMMENT = (
    Regex(r'/\*\*(?:[^*]*\*+)+?/')
)#.setParseAction(parseJavaDoc)
COMMENTS = (
    SINGLE_LINE_COMMENT#.suppress()
    ^ JAVADOC_COMMENT
    ^ MULTI_LINE_COMMENT#.suppress()
)

DBL_QUOTED_STRING = QuotedString(quoteChar="\"", escChar='\\')
SINGLE_QUOTED_STRING = QuotedString(quoteChar="'", escChar='\\')
ARRAY_INIT = LSQUARE + RSQUARE
VALUE = (
    floatnumber ^ QUALIFIED_IDENTIFIER
    ^ DBL_QUOTED_STRING ^ SINGLE_QUOTED_STRING
    ^ integer ^ HEX
)
INIT = (
    QuotedString(quoteChar="=", endQuoteChar=";",multiline=True)
    ^ (EQUAL + DBL_QUOTED_STRING + TERMINATOR)
)
# 作用域相关
USE_NAMESPACE = (
    KEYWORDS['use'].suppress()
    + KEYWORDS['namespace'].suppress()
    + QUALIFIED_IDENTIFIER + TERMINATOR
)
INCLUDE_DEFINITION = (
    KEYWORDS['include']
    + QuotedString(quoteChar="\"", escChar='\\')
    + TERMINATOR
)
IMPORT_DEFINITION = (
    KEYWORDS['import']
    + Combine(
        QUALIFIED_IDENTIFIER
        + Optional(DOT + STAR))('name')
    + TERMINATOR
).setParseAction(parseImports)

ATTRIBUTES = (
    Optional(IDENTIFIER("key") + EQUAL)
    + VALUE("value")
).setResultsName("attributes", listAllMatches=True)
METATAG = (
    LSQUARE   # [
    + IDENTIFIER('name')
    + Optional(LPARN + delimitedList(ATTRIBUTES) + RPARN)
    + RSQUARE # ]
).setParseAction(parseASMetaTag)
BLOCK = Suppress(nestedExpr("{","}"))
# BASE_BLOCK = USE_NAMESPACE ^ COMMENTS ^ METATAG('metatag') ^ INCLUDE_DEFINITION
# 加上静态初始化块
BASE_BLOCK = USE_NAMESPACE ^ INCLUDE_DEFINITION ^ BLOCK
# 变量相关
TYPE = COLON + (QUALIFIED_IDENTIFIER ^ STAR)('type_')
VARIABLE_MODIFIERS = (
    Optional(KEYWORDS['static']('static'))
    & Optional(~KEYWORDS['var'] + IDENTIFIER('visibility'))
)
VARIABLE_DEFINITION = (
    ZeroOrMore(METATAG)('metatag')
    + VARIABLE_MODIFIERS
    + (KEYWORDS['const'] ^ KEYWORDS['var'])("kind")
    + IDENTIFIER('name')
    + Optional(TYPE)
    + Optional(MULTI_LINE_COMMENT)
    + (INIT ^ TERMINATOR)
).setParseAction(parseASVariable)
# 方法相关的语法
METHOD_MODIFIER = (
    Optional(KEYWORDS['static']('static'))
    & (Optional(KEYWORDS['override']("override"))
        & Optional(KEYWORDS['final']('final'))
        & Optional(~KEYWORDS['function'] + IDENTIFIER('visibility'))
    )
)
METHOD_PARAMETER = (
    IDENTIFIER('name')
    + TYPE
    + Optional(EQUAL + VALUE)
).setParseAction(parseASArg)
METHOD_PARAMETERS = delimitedList(METHOD_PARAMETER)#.setDebug()
METHOD_SIGNATURE = (
    KEYWORDS['function']
    # getter, setter
    + Optional(KEYWORDS['get'] ^ KEYWORDS['set'])("accessor")
    # 函数名
    + IDENTIFIER('name')
    + LPARN  # (
    # 以 ',' 分割的参数
    + Optional(METHOD_PARAMETERS('arguments'))
    # ... 任意长参数
    + Optional(Optional(COMMA) + REST + IDENTIFIER)
    + RPARN  # )
    # 返回值类型
    + Optional(TYPE)# + Optional(COMMENTS)
)
METHOD_DEFINITION = (
    Optional(METHOD_MODIFIER)
    + METHOD_SIGNATURE
    + BLOCK
).setParseAction(parseASMethod)#.setDebug()
# 类相关的语法
CLASS_IMPLEMENTS = (
    KEYWORDS['implements']
    + delimitedList(
        QUALIFIED_IDENTIFIER
    ).setResultsName("implements")
)
CLASS_BLOCK = (
    LCURL   # {
    + ZeroOrMore(
        IMPORT_DEFINITION
        ^ BASE_BLOCK
        ^ VARIABLE_DEFINITION.setResultsName('variables', listAllMatches=True)
        ^ METHOD_DEFINITION.setResultsName('methods', listAllMatches=True)
    )
    + RCURL # }
)
CLASS_EXTENDS = KEYWORDS['extends'] + QUALIFIED_IDENTIFIER("extends")
INTERFACE_EXTENDS = KEYWORDS['extends'] + delimitedList(QUALIFIED_IDENTIFIER)
BASE_MODIFIERS = KEYWORDS['internal'] ^ KEYWORDS['public']
CLASS_MODIFIERS = (
    Optional(KEYWORDS['final']('final'))
    & Optional(KEYWORDS['dynamic']('dynamic'))
    & Optional(BASE_MODIFIERS('visibility'))
)
CLASS_DEFINITION = (
    ZeroOrMore(METATAG)('metatag')
    + CLASS_MODIFIERS
    + KEYWORDS['class']
    + QUALIFIED_IDENTIFIER('name')
    + Optional(CLASS_EXTENDS)
    + Optional(CLASS_IMPLEMENTS)
    + CLASS_BLOCK
).setParseAction(parseASClass)
# 接口相关的语法
INTERFACE_BLOCK = (
    LCURL   # {
    + ZeroOrMore(
        IMPORT_DEFINITION
        ^ BASE_BLOCK
        ^ VARIABLE_DEFINITION
        ^ (METHOD_SIGNATURE + TERMINATOR)
    )
    + RCURL # }
)
INTERFACE_DEFINITION = (
    Optional(BASE_MODIFIERS)
    + KEYWORDS['interface'] + QUALIFIED_IDENTIFIER
    + Optional(INTERFACE_EXTENDS)
    + INTERFACE_BLOCK
)
# 包相关的语法
PACKAGE_BLOCK = (
    LCURL   # {
    + ZeroOrMore(IMPORT_DEFINITION)('imports')
    + ZeroOrMore(USE_NAMESPACE)('use_namespace')
    + (CLASS_DEFINITION('class_') ^ INTERFACE_DEFINITION('interface'))
    + RCURL # }
)
PACKAGE_DEFINITION = (
    KEYWORDS['package'].suppress()
    + Optional(QUALIFIED_IDENTIFIER('name'))
    + PACKAGE_BLOCK
).setParseAction(parseASPackage)
# Windows 下文件的 BOM 头
BOM = Literal('\xEF\xBB\xBF').suppress()
PROGRAM = (
    Optional(BOM)
    # + ZeroOrMore(COMMENTS)
    + PACKAGE_DEFINITION
)

