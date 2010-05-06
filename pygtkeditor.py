#!/usr/bin/env python2.5

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
#import pango
import os
import pge_theme
import pge_preferences

gtk.gdk.threads_init()

#from portrait import FremantleRotation
import pge_window
import sys
import pge_report

class PyGTKEditor:

  VERSION = '3.0.17'
  pge_report.install_excepthook("PyGTKEditor", VERSION)

  def __init__(self):

    self.app = hildon.Program()
    self.context = osso.Context('net.khertan.pygtkeditor', self.VERSION, False)
    self.app.set_can_hibernate(True)
    self.window_list = None
    self._manage_theme()
    self.theme = None

    self.prefs = pge_preferences.Prefs()
    self.prefs.load()

    self.load_theme()

    self._last_opened_folder = '/home/user/MyDocs/'

    if self.context:
      self.osso_rpc = osso.Rpc(self.context)
      self.osso_rpc.set_rpc_callback("net.khertan.pygtkeditor", "/net/khertan/pygtkeditor",  "net.khertan.pygtkeditor", self.cb_mime_open, self.context)

    argv = sys.argv
    argv.pop(0)

    for arg in argv:
      self.create_window(os.path.abspath(arg))

    if self.window_list == None:
      import pge_main
      self.window_list = []
      w = pge_main.Window(self)
      self.window_list.append(w)
      self.app.add_window(w)
      w.connect("destroy", self.destroy_win)


  def cb_mime_open(self, interface, method, args, user_data):
    if method!='mime_open':
     return
    try:
      uri=os.path.abspath(args[0])
    except:
     return
    if uri.startswith('file://'):
      self.create_window(uri[7:])

  def onAbout(self, widget):
    import about
    dial = about.Dialog('PyGTKEditor', self.VERSION,  'A source code editor for Maemo' , 'pygtkeditor', 'GPLv2','http://khertan.net/','http://bugs.maemo.org')
    dial.run()
    dial.destroy()

  def _manage_theme(self):
    icons = (( gtk.STOCK_ADD,   "general_add" ),
        ( gtk.STOCK_BOLD,       "general_bold" ),
        ( gtk.STOCK_CLOSE,      "general_close_b" ),
        ( gtk.STOCK_DELETE,     "general_delete" ),
        ( gtk.STOCK_DIRECTORY,  "general_toolbar_folder" ),
        ( gtk.STOCK_FIND,       "general_search" ),
        ( gtk.STOCK_FULLSCREEN, "general_fullsize_b" ),
        ( gtk.STOCK_GO_BACK,    "general_back" ),
        ( gtk.STOCK_GO_FORWARD, "general_forward" ),
        ( gtk.STOCK_GO_UP,      "filemanager_folder_up" ),
        ( gtk.STOCK_GOTO_FIRST, "pdf_viewer_first_page" ),
        ( gtk.STOCK_GOTO_LAST,  "pdf_viewer_last_page" ),
        ( gtk.STOCK_INFO,       "general_information" ),
        ( gtk.STOCK_ITALIC,     "general_italic" ),
        ( gtk.STOCK_JUMP_TO,    "general_move_to_folder" ),
        ( gtk.STOCK_PREFERENCES,"general_settings" ),
        ( gtk.STOCK_REFRESH,    "general_refresh" ),
        ( gtk.STOCK_SAVE,       "notes_save" ),
        ( gtk.STOCK_STOP,       "general_stop" ),
        ( gtk.STOCK_UNDERLINE,  "notes_underline" ),
        ( gtk.STOCK_ZOOM_IN,    "pdf_zoomin" ),
        ( gtk.STOCK_ZOOM_OUT,   "pdf_zoomout" ),
        ( gtk.STOCK_UNDERLINE,  "general_tag"),)

    iconfactory = gtk.IconFactory()

    for stock_id, name in icons:
      iconset = gtk.IconSet()
      iconsource = gtk.IconSource()
      iconsource.set_icon_name(name)
      iconset.add_source(iconsource)
      iconfactory.add(stock_id, iconset)

    iconset = gtk.IconSet(gtk.gdk.pixbuf_new_from_file('/usr/share/icons/hicolor/48x48/hildon/pygtkeditor-increase_indent.png'))
    iconfactory.add(gtk.STOCK_INDENT, iconset)
    iconfactory.add_default()
    iconset = gtk.IconSet(gtk.gdk.pixbuf_new_from_file('/usr/share/icons/hicolor/48x48/hildon/pygtkeditor-decrease_indent.png'))
    iconfactory.add(gtk.STOCK_UNINDENT, iconset)
    iconfactory.add_default()
    return

  def load_theme(self):
    if self.prefs.prefs_dict.has_key('theme'):
        theme_name = self.prefs.prefs_dict['theme']+'.theme'
    else:
        print 'DEFAULT THEME loaded'
        theme_name = 'default.theme'
    self.theme = pge_theme.Theme(theme_name).theme_dict
    return

  def close_win(self, widget,  *data):
    if widget.saved == False:
      noteconf = hildon.hildon_note_new_confirmation(hildon.Window(),'Did you want to save this unsaved file ?')
      if noteconf.run() == gtk.RESPONSE_OK:
        widget.save()
      noteconf.destroy()
    return

  def destroy_win(self, widget,  *data):
    self.window_list.remove(widget)
    if len(self.window_list)==0:
      gtk.main_quit()

  def create_window(self, filepath=None):
    newwin = pge_window.Window(filepath, self,  prefs=self.prefs , theme=self.theme)
    newwin.connect("destroy", self.destroy_win)
    newwin.connect("delete-event", self.close_win)
    if self.window_list==None:
      self.window_list = []
    self.window_list.append(newwin)
    self.app.add_window(newwin)

  def apply_prefs(self):
    self.prefs.load()
    self.load_theme()

    for window in self.window_list:
      window.apply_prefs(self.prefs, self.theme)

if __name__ == "__main__":
  PyGTKEditor()
#  gtk.gdk.threads_enter()
  gtk.main()
#  gtk.gdk.threads_leave()
