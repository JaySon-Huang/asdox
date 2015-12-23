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
from asAction import (
    parseASPackage,
    parseASClass,
    parseASInterface,
    parseASVirtualMethod,
    parseImports,
    parseASMetaTag,
    parseASArg,
    parseASMethod,
    parseASVariable,
)

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
# 标识符, 首字母可以为字母或_或$
IDENTIFIER = Word(alphas+'_'+'$', alphanums+'_')
QUALIFIED_IDENTIFIER = Combine(
    IDENTIFIER
    + ZeroOrMore(DOT + IDENTIFIER)
)
# 泛型
GENERIC_IDENTIFIER = Combine(
    IDENTIFIER
    + ZeroOrMore(DOT + '<' + IDENTIFIER + '>')
)
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
OBJECT_INIT = nestedExpr("{","}")
VALUE = (
    floatnumber ^ QUALIFIED_IDENTIFIER
    ^ DBL_QUOTED_STRING ^ SINGLE_QUOTED_STRING
    ^ integer ^ HEX
)
INIT = (
    QuotedString(quoteChar="=", endQuoteChar=";", multiline=True)
    ^ (
        EQUAL
        + (DBL_QUOTED_STRING ^ ARRAY_INIT ^ OBJECT_INIT)
        + TERMINATOR
    )
)
# 作用域相关
USE_NAMESPACE = (
    KEYWORDS['use'].suppress()
    + KEYWORDS['namespace'].suppress()
    + QUALIFIED_IDENTIFIER + TERMINATOR
)
NAMESPACE_DEFINITION = (
    Optional(KEYWORDS['public'])
    + KEYWORDS['namespace']
    + IDENTIFIER('name')
    + TERMINATOR
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
# 变量相关
TYPE = COLON + (QUALIFIED_IDENTIFIER ^ GENERIC_IDENTIFIER ^ STAR)('type_')
VARIABLE_MODIFIERS = (
    Optional(KEYWORDS['static']('static'))
    & Optional(~KEYWORDS['var'] + ~KEYWORDS['const'] + IDENTIFIER('visibility'))
)
VARIABLE_DEFINITION = (
    ZeroOrMore(METATAG)('metatag')
    + VARIABLE_MODIFIERS
    + (KEYWORDS['const'] ^ KEYWORDS['var'])("kind")
    + IDENTIFIER('name')
    + Optional(TYPE)
    # + Optional(MULTI_LINE_COMMENT)
    + (INIT ^ TERMINATOR)
).setParseAction(parseASVariable)
VARIABLE_INITIALIZATION = (
    IDENTIFIER('name')
    + (INIT ^ TERMINATOR)
)
BLOCK = Suppress(nestedExpr("{","}"))
# BASE_BLOCK = USE_NAMESPACE ^ COMMENTS ^ METATAG('metatag') ^ INCLUDE_DEFINITION
# 加上静态初始化块
BASE_BLOCK = USE_NAMESPACE ^ INCLUDE_DEFINITION ^ BLOCK ^ VARIABLE_INITIALIZATION
# 方法相关的语法
METHOD_MODIFIER = (
    Optional(KEYWORDS['static']('static'))
    & (Optional(KEYWORDS['override']('override'))
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
    ZeroOrMore(METATAG)('metatag')
    + Optional(METHOD_MODIFIER)
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
CLASS_EXTENDS = KEYWORDS['extends'] + QUALIFIED_IDENTIFIER('extends')
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
        ^ VARIABLE_DEFINITION.setResultsName('variables', listAllMatches=True)
        ^ (METHOD_SIGNATURE + TERMINATOR).setParseAction(
                parseASVirtualMethod
            ).setResultsName(
                'methods', listAllMatches=True
            )
    )
    + RCURL # }
)
INTERFACE_DEFINITION = (
    Optional(BASE_MODIFIERS)
    + KEYWORDS['interface']
    + QUALIFIED_IDENTIFIER('name')
    + Optional(INTERFACE_EXTENDS)
    + INTERFACE_BLOCK
).setParseAction(parseASInterface)
# 包相关的语法
PACKAGE_BLOCK = (
    LCURL   # {
    + ZeroOrMore(IMPORT_DEFINITION)('imports')
    + ZeroOrMore(USE_NAMESPACE)('use_namespace')
    + (
        CLASS_DEFINITION('class_')
        ^ INTERFACE_DEFINITION('interface')
        ^ NAMESPACE_DEFINITION
    )
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

