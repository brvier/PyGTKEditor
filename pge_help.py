#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

#
# PyGTKEditor
#
# Copyright (c) 2007 Khertan (Benoit HERVIER)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#        
# Khertan (Benoit HERVIER) khertan@khertan.net

import hildon
import gtk
import osso
import pango
from portrait import FremantleRotation
import os

class Help(hildon.Window):
  def __init__(self,filepath=None,caller=None):
    hildon.Window.__init__ (self)
    FremantleRotation('net.khertan.pygtkeditor',self)
    
    p = hildon.PannableArea()
    t = hildon.TextView()
    t.set_editable(False)
    t.get_buffer().set_text(u"""PyGTKEditor is a source code editor, specially designed for Maemo Devices.

Report bugs on http://bugs.maemo.org/
For any comments do not hesitate to contact me at : khertan@khertan.net

Shortcuts :
• Ctrl-O : Open file
• Ctrl-S : Save file
• Ctrl-W : Close file
• Ctrl-I : Show file info
• Ctrl-C : Copy
• Ctrl-C : Cut
• Ctrl-V : Paste
• Ctrl-Z : Undo
• Ctrl-Y : Redo
• Ctrl-D : Duplicate Line
• Ctrl-F : Find
• Ctrl-R : Replace
• Ctrl-A : Select All
• Ctrl-E : Execute
• Ctrl-H : Show help

Hilighted "Languages":
• R
• Ada
• C
• Changelog
• C++
• CSharp
• Desktop (.desktop)
• Css
• Diff (diff)
• Fortran
• Gtkrc
• Haskell
• Html
• Idl
• Ini (.ini)
• Java
• Javascript
• Latex
• Lua
• Makefile
• Markdown
• Msil
• Nemerle
• Octave
• Pascal
• Perl
• Php
• Po
• Python
• Ruby
• Scheme
• Sh
• Tcl
• Texinfo
• Vbnet
• Verilog
• Vhdl
• Xml

Roadmap :

• Version 3.0.1 :
◦ Prefs : indent size
◦ Prefs : font and text size
◦ Welcome screen

• Version 3.1.0 :
◦ Prefs : indent size
◦ Prefs : font and text size
◦ Welcome screen

•Version 3.3.0 :
◦ Plugins
◦ Snippet
""")
    p.add(t)
    self.add(p)
    
    self.show_all()