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
import pge_preferences

class Help(hildon.Window):
  def __init__(self,filepath=None,caller=None):
    hildon.Window.__init__ (self)
    self.set_title('PyGTKEditor - Help')
    self.prefs = pge_preferences.Prefs()
    self.prefs.load()

    if self.prefs.prefs_dict['auto_rotate']==True:
      self.rotation = FremantleRotation('net.khertan.pygtkeditor',self,mode=FremantleRotation.AUTOMATIC)
    else:
      self.rotation = FremantleRotation('net.khertan.pygtkeditor',self,mode=FremantleRotation.NEVER)

    p = hildon.PannableArea()
    t = hildon.TextView()
    t.set_editable(False)
    t.set_wrap_mode(gtk.WRAP_WORD)
    t.get_buffer().set_text(u"""PyGTKEditor is a source code editor, specially designed for Maemo Devices.

Report bugs or feature request on http://khertan.net/flyspray/

Shortcuts :
• Ctrl-N : New file
• Ctrl-O : Open file
• Ctrl-S : Save file
• Ctrl-W : Close file
• Ctrl-I : Show file info
• Ctrl-C : Copy
• Ctrl-X : Cut
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
◦ Fix Bug #6397
◦ Fix Bug #6399
◦ Implement simple cacher in parser
◦ Fix icon in open dialog

• Version 3.0.2 :
◦ Prefs : default language
◦ Prefs : default language
◦ Prefs : Auto rotate option
◦ Prefs : font and text size
◦ Prefs : enable or not word completion
◦ Fix Bug #6522
◦ Fix Bug #6547
◦ Fix Bug #7021

• Version 3.0.3 :
◦ Fix Help Bug

• Version 3.0.4 :
◦ Prefs : indent size
◦ Welcome screen
◦ Recent Chooser Change
◦ Prefs show lines numbers

• Version 3.0.5 :
◦ Fix 2 syntax errors

• Version 3.0.6 :
◦ Fix None default language : #8074
◦ Detect .txt as text file (no syntax hilight)

• Version 3.0.7 :
◦ Fix uncomplete preference file
◦ Fix icon in package
◦ Fix help windows title

• Version 3.0.8 :
◦ Fix syntax error

• Version 3.0.9 :
◦ Keep last opened folder when opening or saving file instead of going to MyDocs folder by default
◦ Remove saveas menu from welcome screen
◦ Fix Bug #8837
◦ Add errors message when not able to open or decode file
◦ Fix apply prefs for lines numbers
◦ Fix recent file change in main
◦ Fix back to begin search when there is 2 results only
◦ Fix order of recent files

•Version 3.0.10 :
◦ Fix help text (Wrong shortcut for cut)
◦ Fix welcome screen new button bug

•Version 3.0.11 :
◦ Fix CTRL-S shortcut
◦ Fix html syntax

•Version 3.0.12 :
◦ Link to bugtracker
◦ Some minor fix due to check with pylint
◦ Fix settings window title : #9001
◦ Fix about menu : #9326
◦ Fix line number : #8814

•Version 3.0.13 :
◦ Link to bugtracker
◦ Implement autoclean space at end of line feature

•Version 3.0.14 :
◦ Fix duplicate multiple lines feature
◦ Fix line number : #8814

•Version 3.0.15 :
◦ Crash reporter implemented to reports bug to my own Bug Tracker System
◦ Package is now provided on my own repository
◦ Add themes support
◦ Add ctrl-n shortcut

•Version 3.0.16 :
◦ Fix Crash reporter
◦ Fix execute toolbar button when trying to execute new file
◦ Fix invalid search pattern error

•Version 3.0.17 :
◦ Fix Bug #19

•Version 3.3.0 :
◦ Plugins
◦ Snippet
""")
    p.add(t)
    self.add(p)

    self.show_all()
