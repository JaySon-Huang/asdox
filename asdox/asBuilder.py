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
import asGrammar,os,fnmatch,asModel

class Builder:
	"Actionscript Source Builder"
	sources = list()
	packages = {}
	def __init__(self):
		self.sources[:] = []
		self.packages = {}
	def addSource(self,source,pattern = "*.as"):
		try:
			try:
				# If 'source' is a file object read it.
				self.parseSource( source.read() )
			except:
				# If 'source' is a filename open and read file.
				self.parseSource( open(source,"r").read() )
		except IOError:
			# If 'source' is a directory read all files matching the
			# specified pattern.
			if os.path.isdir( source ):
				files = self.locate(pattern,source)
				for f in files:
					self.parseSource( open(f,"r").read() )
			else:
				# If 'source' is a string append to source list
				self.parseSource( source )
	def parseSource(self,src):
		self.sources.append( src )
		asGrammar.PROGRAM.parseString(src.decode("ascii","ignore"))
		pkg = asGrammar.package
		asGrammar.package = asModel.ASPackage()
		
		if pkg.name in self.packages:
			for imp in pkg.imports:
				if imp not in self.packages[pkg.name].imports:
					self.packages[pkg.name].imports.append(imp)
			for cls in pkg.classes.values():
				self.packages[pkg.name].classes[cls.name] = cls
		else:
			self.packages[pkg.name] = pkg
	def locate(self,pattern, root=os.getcwd()):
		for path, dirs, files in os.walk(root):
			for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
				yield filename