ColorStr
--------

String type object that override basic str, usefull for printing colored
strings in console (if Ansi compatible)

Main str method are overrided and return colored string, other methods
simply use plain str text (see source code for details)
The % operator use some workaround to work with Colorstr
if you see strange behaviors please [open a issue](https://github.com/loggerhead/ColorStr/issues), thanks


Colors and attributes use same sintax of ANSI string:
    \033[<attributes list>m


WARNING: Do not use `ColorStr` as `str` ! Please use it just need printing
colored strings. Invoke any function will convert `ColorStr` to `str`

Get color str

    ColorStr(string[, color1, color2, ...])

Get plain text from string use

    ColorStr.get_plain(string)

#Examples

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
