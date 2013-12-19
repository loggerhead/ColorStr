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

"""
ColorStr

String type object that override basic str, usefull for printing colored
strings in console (if Ansi compatible)

Main str method are overrided and return colored string, other methods
simply use plain str text (see source code for details)
The % operator use some workaround to work with Colorstr
if you see strange behaviors please open a issue, thanks
<https://github.com/loggerhead/ColorStr/issues>

Colors and attributes use same sintax of ANSI string:
    \033[<attributes list>m
"""


class ColorStr(str):
    """
    WARNING: Do not use `ColorStr` as `str` ! Please use it just need printing
    colored strings. Invoke any function will convert `ColorStr` to `str`

    Get color str

        ColorStr(string[, color1, color2, ...])

    Get plain text from string use

        ColorStr.get_plain(string)

    See more examples below

    """
    _special = {
        'start': '\033[', 'reset': '\033[0m',
    }
    _color = {
        'underline': 4,
        # reverse forecolor and backcolor
        'reverse': 7,
        'normal': 0, 'bright': 1, 'bold': 1, 'dark': 2,
        'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
        'blue':34, 'magenta': 35, 'cyan': 36, 'white': 37,
    }

    for key, value in _color.items():
        _color['f_' + key] = value
        _color['b_' + key] = value + 10

    def __new__(cls, text='', *colors):
        colors = [c.lower() for c in colors]
        all_colors = set(cls._color.keys())
        if not set(colors).issubset(all_colors):
            raise Exception('invalid colors')

        text = cls.render(text, *colors)
        return str.__new__(cls, text)

    def __init__(self, text='', *colors):
        self.text = text
        self.colors = colors

    @classmethod
    def render(cls, text, *colors):
        start = cls.get_render_code(*colors)
        end = cls._special['reset']
        return start + text + end

    @classmethod
    def get_render_code(cls, *colors):
        render_str = ';'.join([str(cls._color[c.lower()]) for c in colors])
        start = cls._special['start'] + render_str + 'm'
        return start

    @classmethod
    def get_plain(cls, color_str):
        if isinstance(color_str, ColorStr):
            return color_str.text
        import re
        pattern = re.compile('\033\\[(\\d+;)*\\d+m')
        plainstr = re.sub(pattern, '', color_str)
        return plainstr

    def escape_args(self, args):
        if not hasattr(self, 'render_code'):
            self.render_code = self.get_render_code(*self.colors)
        start = self.render_code
        end = self._special['reset']
        newargs = tuple([(end + arg + start) for arg in args])
        return newargs

    def escape_kwargs(self, kwargs):
        if not hasattr(self, 'render_code'):
            self.render_code = self.get_render_code(*self.colors)
        start = self.render_code
        end = self._special['reset']
        newkwargs = {}
        for key, value in kwargs.items():
            newkwargs[key] = end + value + start
        return newkwargs

    def __mod__(self, args):
        if isinstance(args, basestring):
            args = (args,)
        newargs = self.escape_args(args)
        return super(ColorStr, self).__mod__(newargs)

    def format(self, *args, **kwargs):
        if isinstance(args, basestring):
            args = (args,)
        newargs = self.escape_args(args)
        newkwargs = self.escape_kwargs(kwargs)
        return super(ColorStr, self).format(*args, **kwargs)


if __name__ == '__main__':
    s = ColorStr('az {0} {foo}', 'red').format('0', foo='I am foo')
    # should be `False` but `True`
    print(s < 'aa')
    # 'f_' means 'foreground', 'b_' means 'background'
    s = ColorStr('%s string', 'f_green', 'b_black') % 'green'
    print(s)
    s = ColorStr('%s string', 'green',
      'bold', 'underline', 'reverse') % ColorStr('green', 'green')
    print(s)
    # invoke any function will turn `ColorStr` to `str`
    print(type(s))
    # `startswith` `find` `len` and other function will mess
    print(s.startswith('green'))
    print(len(s))
    print(s == 'green string')
    # use `ColorStr.get_plain` get plain text
    s = ColorStr.get_plain(s)
    print(s)
