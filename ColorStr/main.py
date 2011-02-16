# -*- coding: utf-8 -*-

# Big thanks to Fabiano Francesconi <elbryan>
# for proving a basic version of this library

# Copyright (c) 2011-2012, Walter Da Col <walter.dacol@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__DOC__ = r"""
str object with color attributes

Main str method are overrided and return ansi colored string,
other methods simply use plain str text (see source code for 
details)
The % operator use some workaround to work with Colorstr, if you see
strange behaviors please mail me, thanks.

To get plain text use object.__repr__() 

Colors and attributes use same sintax of Ansi string:
\033[<attributes list>m"""

__VERSION__ = '0.2'

# EXCEPTION

class DefaultException(Exception):
	def __init__(self,value=''):
		self.value = value
		
	def __str__(self):
		return repr(self.value)

class NotImplemendYet(DefaultException):
	""" Not implemented """

# ANSI SEQUENCES

COLOR_ANSI = '\033['
RESET_ANSI = COLOR_ANSI+'0m'

# ANSI COLOR VALUE
F_BLACK, F_RED, F_GREEN, F_YELLOW, F_BLUE, F_MAGENTA, F_CYAN, F_WHITE = range(30, 38)
B_BLACK, B_RED, B_GREEN, B_YELLOW, B_BLUE, B_MAGENTA, B_CYAN, B_WHITE = range(40, 48)
BRIGHT = 1
UNDERLINE = 4
DARK = 2
NORMAL = 0

# COLOR SEQUENCES AND FUNCTIONS

def getColorSeq(ansiColors=[0]):
	if type(ansiColors) != list:
			raise NotValidAnsiColors(type(ansiColors))
	return COLOR_ANSI + ''.join([str(item)+';' for item in ansiColors[:-1]])+str(ansiColors[-1]) + 'm'
	
def black(text): return getColorSeq([F_BLACK])+text+RESET_ANSI
def red(text): return getColorSeq([F_RED])+text+RESET_ANSI
def green(text): return getColorSeq([F_GREEN])+text+RESET_ANSI
def yellow(text): return getColorSeq([F_YELLOW])+text+RESET_ANSI
def blue(text): return getColorSeq([F_BLUE])+text+RESET_ANSI
def magenta(text): return getColorSeq([F_MAGENTA])+text+RESET_ANSI
def cyan(text): return getColorSeq([F_CYAN])+text+RESET_ANSI
def white(text): return getColorSeq([F_WHITE])+text+RESET_ANSI
def bright(text): return getColorSeq([BRIGHT])+text+RESET_ANSI
def dark(text): return getColorSeq([DARK])+text+RESET_ANSI

# COLORSTR CLASS

class ColorStr(str):
	def __new__(self,text,ansiColors=[0]):
		return str.__new__(self,text)
	
	def __init__(self,text,ansiColors):
		"""
		@param text: what will be printed
		@type text: any type supported by str() method (eg. str, int, ..)
		@param ansi_colors: console ANSI modifier(see source code) values
		@type ansi_colors: int list
		"""
		if type(ansiColors) != list:
			raise NotValidAnsiColors(type(ansiColors))
		self.colorString = '\033['+''.join([str(item)+';' for item in ansiColors[:-1]])+str(ansiColors[-1])+'m'
	
	def _modFixer(self,args):
		"""
		Fix string formatter, in case you use Colorstr in args
		"""
		validType = [dict,tuple,ColorStr]
		if type(args) not in validType:
			return args
		newArgs = None
		if type(args)==dict:
			newArgs = {}
			for key in args:
				if type(args[key]) == ColorStr:
					newArgs.update({key:(args[key]+self.colorString)})
				else:
					newArgs.update({key:args[key]})
			return newArgs
		if type(args)==tuple:
			newArgs = ()
			for item in args:
				if type(item) == ColorStr:
					newArgs = newArgs + (item+self.colorString,)
				else:
					newArgs = newArgs + (item,)
			return newArgs
		return str(args)+self.colorString
	
	def __repr__(self):
		return str.__str__(self)

	def __str__(self):
		return self.colorString+str.__str__(self)+RESET_ANSI

	def __mod__(self,args):
		newArgs = self._modFixer(args)
		return self.colorString+(str.__str__(self) % newArgs)+RESET_ANSI

	def __add__(self,value):
		return self.__str__() + value
		
	def __radd__(self,value):
		return value + self.__str__()

	def __format__(self,args):
		raise NotImplemendYet('__format__')

	def format(self,args):
		raise NotImplemendYet('format')

	def __getslice__(self,a,b):
		return self.colorString+str.__getslice__(self,a,b)+RESET_ANSI

	def __mul__(self,value):
		return self.colorString+(str.__mul__(self,value))+RESET_ANSI

	def __rmul__(self,value):
		return self.colorString+(str.__rmul__(self,value))+RESET_ANSI

	def replace(self,pattern,replace):
		return self.colorString+(str.replace(self,pattern,replace+self.colorString))+RESET_ANSI

	def __doc__(self):
		print __DOC__

if __name__ == '__main__':
	print ColorStr('# ColorStr %s #',[B_GREEN,F_BLACK,UNDERLINE]) % __VERSION__
	print ColorStr(__DOC__,[F_CYAN])
	print

	t_str = ColorStr('This %s a %s',[F_GREEN])
	t_is = ColorStr('is',[B_GREEN,F_BLACK])
	t_test = ColorStr('Test',[F_WHITE,B_YELLOW])
	
	print t_str % (t_is,t_test)
