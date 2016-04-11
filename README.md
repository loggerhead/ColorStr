#ColorStr
A subclass of `str`, useful for printing colored strings in console (if ANSI compatible).

-------

Recommend you to use a better alternate like: [termcolor](https://pypi.python.org/pypi/termcolor), [colorama](https://pypi.python.org/pypi/colorama)

#Notice
`%` `format` is override, but other `str` function is mess (see [examples](#examples) or [source code](https://github.com/loggerhead/ColorStr/blob/master/colorstr.py) for details). So... Do __NOT__ use `ColorStr` as `str`! Calling any function will convert `ColorStr` to `str`.

#Usage

colors: `underline` `reverse` `normal` `bright` `bold` `dark` `black` `red` `green` `yellow` `blue` `magenta` `cyan` `white`
    
    ColorStr(string[, color1, color2, ...])
    
Get color str    

```python
cs = ColorStr('hello, world', 'blue', 'b_white')
print(cs)
```

Turn `ColorStr` to normal `str`

```python
ColorStr.get_plain(string)
```

#Examples

```python
from colorstr import ColorStr

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
```
