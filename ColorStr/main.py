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

""" ColorStr

String type object that override basic str, usefull for printing colored
strings in console (if Ansi compatible)

Main str method are overrided and return colored string, other methods
simply use plain str text (see source code for details)
The % operator use some workaround to work with Colorstr, if you see
strange behaviors please mail me, thanks.

To get plain text use
    Colorstr.__repr__()

Colors and attributes use same sintax of Ansi string:
    \033[<attributes list>m """

__VERSION__ = '0.2'

# EXCEPTION

class DefaultException(Exception):
    """ A general exception with a string parameter """

    def __init__(self,value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NotImplemendYet(DefaultException):
    """ Not implemented """

class NotValidAnsiColors(DefaultException):
    """ Invalid escape sequence """

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

def get_color_seq(ansi_colors=[0]):
    """ Returns Ansi escape sequence

        @param ansi_colors: List of colors
        @type ansi_colors: Lost of colors (see above for the list) """

    if type(ansi_colors) != list:
            raise NotValidAnsiColors(type(ansi_colors))
    return COLOR_ANSI + ''.join([str(item)+';' for item in ansi_colors[:-1]])+str(ansi_colors[-1]) + 'm'

def black(text):
    """ Returns a colored string

        @param text: input string
        @type text: string """

    return get_color_seq([F_BLACK])+text+RESET_ANSI

def red(text):
    """ Returns a colored string

        @param text: input string
        @type text: string """

    return get_color_seq([F_RED])+text+RESET_ANSI

def green(text):
    """ Returns a colored string

        @param text: input string
        @type text: string """

    return get_color_seq([F_GREEN])+text+RESET_ANSI

def yellow(text):
    """ Returns a colored string

        @param text: input string
        @type text: string """

    return get_color_seq([F_YELLOW])+text+RESET_ANSI

def blue(text):
    """ Returns a colored string

        @param text: input string
        @type text: string """

    return get_color_seq([F_BLUE])+text+RESET_ANSI

def magenta(text):
    """ Returns a colored string

        @param text: input string
        @type text: string """

    return get_color_seq([F_MAGENTA])+text+RESET_ANSI

def cyan(text):
    """ Returns a colored string

        @param text: input string
        @type text: string """

    return get_color_seq([F_CYAN])+text+RESET_ANSI

def white(text):
    """ Returns a colored string

        @param text: input string
        @type text: string """

    return get_color_seq([F_WHITE])+text+RESET_ANSI

def bright(text):
    """ Returns a colored string

        @param text: input string
        @type text: string """

    return get_color_seq([BRIGHT])+text+RESET_ANSI

def dark(text):
    """ Returns a colored string

        @param text: input string
        @type text: string """

    return get_color_seq([DARK])+text+RESET_ANSI


# COLORSTR CLASS

class ColorStr(str):

    # If false will disable colors
    __enabled = True

    @classmethod
    def configure(cls, enable_color=True):
        """ Set class for using (or not) colors """
        cls.__enabled = enable_color

    @classmethod
    def __new__(cls, self, text, ansi_colors=[0]):
        return str.__new__(cls, text)

    def __init__(self, text, ansi_colors):
        """
        @param text: what will be printed
        @type text: any type supported by str() method (eg. str, int, ..)
        @param ansi_colors: console ANSI modifier(see source code) values
        @type ansi_colors: int list
        """
        if type(ansi_colors) != list:
            raise NotValidAnsiColors(type(ansi_colors))
        self.color_str = '\033['+''.join([str(item)+';' for item in ansi_colors[:-1]])+str(ansi_colors[-1])+'m'

    def __mod_fixer(self, args):
        """
        Fix string formatter, in case you use Colorstr in args
        """
        valid_type = [dict, tuple, ColorStr]
        if type(args) not in valid_type:
            return args
        new_args = None
        if type(args) == dict:
            new_args = {}
            for key in args:
                if type(args[key]) == ColorStr:
                    new_args.update({key:(args[key]+self.color_str)})
                else:
                    new_args.update({key:args[key]})
            return new_args
        if type(args) == tuple:
            new_args = ()
            for item in args:
                if type(item) == ColorStr:
                    new_args = new_args + (item+self.color_str,)
                else:
                    new_args = new_args + (item,)
            return new_args
        return str(args)+self.color_str

    def __repr__(self):
        return str.__str__(self)

    def __str__(self):
        if self.__enabled:
            return self.color_str+str.__str__(self)+RESET_ANSI
        else:
            return self.__repr__()

    def __mod__(self, args):
        if not self.__enabled:
            return self.__repr__() % args
        new_args = self.__mod_fixer(args)
        return self.color_str+(str.__str__(self) % new_args)+RESET_ANSI

    def __add__(self, value):
        if not self.__enabled:
            return self.__repr__() + value
        return self.__str__() + value

    def __radd__(self, value):
        if not self.__enabled:
            return value + self.__repr__()
        return value + self.__str__()

    def __format__(self, args):
        raise NotImplemendYet('__format__')

    def format(self, args):
        raise NotImplemendYet('format')

    def __getslice__(self, first_arg, second_arg):
        if not self.__enabled:
            return self.__repr__().__getslice__(first_arg, second_arg)
        return self.color_str+str.__getslice__(self, first_arg, second_arg)+RESET_ANSI

    def __mul__(self, value):
        if not self.__enabled:
            return self.__repr__().__mul__(value)
        return self.color_str+(str.__mul__(self, value))+RESET_ANSI

    def __rmul__(self, value):
        if not self.__enabled:
            return self.__repr__().__rmul__(value)
        return self.color_str+(str.__rmul__(self, value))+RESET_ANSI

    def replace(self, pattern, replace):
        if not self.__enabled:
            return self.__repr__().replace(pattern, replace)
        return self.color_str+(str.replace(self, pattern, replace+self.color_str))+RESET_ANSI

    def __doc__(self):
        print __DOC__

if __name__ == '__main__':

    print ColorStr('# ColorStr %s #', [B_GREEN, F_BLACK, UNDERLINE]) % __VERSION__
    print

    t_str = ColorStr('This %s a %s', [F_GREEN])
    t_is = ColorStr('is', [B_GREEN, F_BLACK])
    t_test = ColorStr('Test', [F_WHITE, B_YELLOW])

    print t_str % (t_is, t_test)
