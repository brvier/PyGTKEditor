#!/usr/bin/python
# -*- coding: utf-8 -*-
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 2 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
import pypackager
import os

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        pass

    p=pypackager.PyPackager("pygtkeditor")
    p.version='3.0.16'
    p.buildversion='1'
    p.display_name='PyGTKEditor'
    p.description="PyGTKEditor is a source code editor specially designed for devices running Maemo."
    p.author="Benoît HERVIER"
    p.maintainer="Khertan"
    p.email="khertan@khertan.net"
    p.depends = "python2.5-hildon,python2.5-gtk2,python-osso,python2.5-xml,python-dbus,python-gobject"
    p.section="user/development"
    p.arch="armel"
    p.urgency="low"
    p.bugtracker='http://khertan.net/flyspray/index.php?project=2'
    p.distribution="fremantle"
    p.repository="extras-devel"
    p.icon='pygtkeditor.png'
    p["/usr/bin"] = ["pygtkeditor",]
    p["/usr/share/dbus-1/services"] = ["pygtkeditor.service",]
    p["/usr/share/pixmaps"] = ["pygtkeditor.png",]
    p["/usr/share/applications/hildon"] = ["pygtkeditor.desktop",]
    p["/usr/share/mime/packages"] = ["cpp-mime.xml",
                                     "glade-mime.xml",
                                     "latex-mime.xml",
                                     "perl-mime.xml",
                                     "cpp-mime.xml",
                                     "xml-mime.xml",
                                     "sql-mime.xml",
                                     "sh-mime.xml",
                                     "ruby-mime.xml",
                                     "python-mime.xml",]
    files = [ "pygtkeditor.py",
                              "pge_window.py",
                              "about.py",
                              "pge_main.py",
                              "pge_recentchooser.py",
                              "pge_buffer.py",
                              "pge_editor.py",
                              "pge_defering.py",
                              "pge_help.py",
                              "pge_preferences.py",
                              "portrait.py",
                              "pge_theme.py",
                              "pge_report.py",
                              "pygtkeditor.png"]

    #Syntax
    for root, dirs, fs in os.walk('/home/user/MyDocs/Projects/pygtkeditor/syntax'):
      for f in fs:
        print os.path.basename(f)
        files.append('syntax/'+os.path.basename(f))
    print files

    #Theme
    for root, dirs, fs in os.walk('/home/user/MyDocs/Projects/pygtkeditor/themes'):
      for f in fs:
        print os.path.basename(f)
        files.append('themes/'+os.path.basename(f))
    print files


    p["/opt/pygtkeditor"] = files

    p["/usr/share/icons/hicolor/48x48/hildon"] = ["pygtkeditor-decrease_indent.png",
                                                  "pygtkeditor-increase_indent.png",]
    p.postinstall = """#!/bin/sh
chmod +x /usr/bin/pygtkeditor
python -m compileall /home/opt/pygtkeditor"""

    p.changelog="""
◦ Fix Crash reporter
◦ Fix execute toolbar button when trying to execute new file
◦ Fix invalid search pattern error
"""
print p.generate(build_binary=False,build_src=True)
print p.generate(build_binary=True,build_src=False)
