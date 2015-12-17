# Introduction #

This is a very simple example of how to use asDox with Cheetah to create a C# object from an Actionscript 3 object.


# Example #

```
from Cheetah.Template import Template
from asdox import asBuilder

builder = asBuilder.Builder()
builder.addSource("""
package com.gurufaction.myApp
{
	public class MyClass
        {
        	private var _name:String;
                private var _age:int;
                
                public function get name():String
                {
                	return _name;
                }
                
                public function set name(value:String):void
                {
                	_name = value;
                }
                
                // Age Property is Read-Only
                public function get age():int
                {
                	return _age;
                }
                
        }
}
""")

pkg = builder.packages["com.gurufaction.myApp"]

c_sharp_template = """
using System;

namespace $pkg.name
{
	#for $key,$cls in $pkg.classes.items()
        #if $cls.visibility == "public"
        public class $cls.name
        {
        	#for $key,$value in $cls.properties.items()
                private $value.type _$value.name.lower();
                #end for
                
        	#for $key,$value in $cls.properties.items()
                #if $value.visibility == "public"
                public $value.type $value.name
                {
                	#if $value.readable
                        get { return _$value.name.lower(); }
                        #end if
                        #if $value.writable
                        set { _$value.name.lower() = value; }   
                        #end if
                }
                
                #end if
                #end for
        }
        #end if
        #end for
}
"""
nameSpace = {'pkg': pkg}
t = Template(c_sharp_template, searchList=[nameSpace])
print t
```
### Output ###
```
using System;

namespace com.gurufaction.myApp
{
        public class MyClass
        {
                public int age
                {
                        get { return _age; }
                }
                
                public String name
                {
                        get { return _name; }
                        set {  _name = value; }   
                }
                
        }
}
```