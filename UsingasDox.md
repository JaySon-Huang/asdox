# Using asDox #

## Entry Point ##

The Builder class is the main entry point for asDox. The Builder class parses source files and generates a model from those source files. The following code demonstrates how to create an instance of the Builder class:

```
from asdox import asBuilder

builder = asBuilder.Builder()
```

## Adding Source Files ##

After creating an instance of the Builder class you need to add Actionscript source files in order to generate a working model. The Builder class has an `addSource()` method for doing this. This method can take a string parameter representing Actionscript code, a filename, a directory, or a file object. When specifying a directory parameter to `addSource` asDox will automatically locate all files with a .as extension in the main directory and any subdirectories.

```
builder.addSource("""
package com.googlecode.asdox
{
	public class MyClass
	{
	}
}
""")

builder.addSource("com\\googlecode\\asdox\\MyClass.as")
builder.addSource("com\\googlecode\\asdox\\")

f = Open("com\\googlecode\\asdox\\MyClass.as")
builder.addSource(f)
```

## Navigating the Model ##

Once all of your source files have been added to the Builder class you can begin navigating the model. The model consist of a hierarchy of objects that represent an Actionscript source file:

  * Package
    * Metadata
    * Class/Interface
      * Metadata
      * Fields/Methods


The Builder class stores package information is a dictionary named `packages`. You can access individual packages using Pythons dictionary notation.

```
pkg = builder.packages["com.googlecode.asdox"]
```

If you don't know the name of the package or if your model contains several packages you can use the `packages` property of the Builder class to get all packages contained in the model. This property returns a dictionary of packages with the key being the package name.

```
for pkg in builder.packages.keys():
	print pkg
```

### Exploring Packages ###

The Package object contains methods for accessing import and class information. If you want to test for the existence of an import statement you can use Python's build in set methods.

```
if( "mx.controls" in pkg.imports ):
        print "mx.controls import found!"
```

You can also retrieve a list of all imports using the `imports` property of the Package class. This property returns a `set()` containing all the import statements.

```
for stmt in pkg.imports:
	print stmt
```

Accessing class information is similar to accessing import information. You can test for the existence of a class using Python's built in dictionary methods.

```
if( "MyClass" in pkg.classes ):
       print pkg.classes["MyClass"].name
```

Or you can access a specific class directly

```
cls = pkg.classes["MyClass"]
```

As with imports you can get retrieve all classes in a package using the `classes` property.

```
for cls in pkg.classes.keys():
       print cls
```