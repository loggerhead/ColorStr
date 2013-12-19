# ColorStr

String type object that override basic str, usefull for printing colored
strings in console (if Ansi compatible)

Main str method are overrided and return colored string, other methods 
simply use plain str text (see source code for details)
The % operator use some workaround to work with Colorstr, if you see
strange behaviors please mail me, thanks.

To get plain text use
    Colorstr.__repr__() 

Colors and attributes use same sintax of Ansi string:
    \033[<attributes list>m


Walter Da Col <walter.dacol AT gmail.com>
