#!/usr/bin/env python
# encoding=utf-8

from pyparsing import ParseResults
from asModel import (
    ASClass, ASPackage, ASMetaTag,
    ASVirtualMethod, ASMethod,
    ASType, ASVariable,
)

_isTracing = False
# _isTracing = True

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

def parseASInterface(s, location, tokens):
    if _isTracing:
        print('parseASInterface[{0}] @ loc({1})'.format(tokens.name, location))
    cls = ASClass(tokens.name)
    # methods
    for method in tokens.methods:
        method = method[0]
        cls.methods[method.name] = method
        # TODO: getter/setter 对相关变量属性进行设置
    # from IPython import embed;embed();
    return ParseResults(cls)

def parseASVirtualMethod(s, location, tokens):
    if _isTracing:
        print('parseASVirtualMethod[{0}] @ loc({1})'.format(tokens.name, location))
    if tokens.type_:
        method = ASVirtualMethod(tokens.name, tokens.type_)
    else:
        method = ASVirtualMethod(tokens.name)
    # method 传入参数
    for arg in tokens.arguments:
        method.arguments[arg.name] = arg
    return ParseResults(method)

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
        print('parseASMethod[{0}] @ loc({1})'.format(tokens.name, location))
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

