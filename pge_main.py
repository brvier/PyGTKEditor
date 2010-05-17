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
import pango
from portrait import FremantleRotation
import pge_editor
import os
from subprocess import *
import commands
import gobject
import pge_preferences
import pge_recentchooser

class Window(hildon.Window):
  def __init__(self,caller=None):
    hildon.Window.__init__ (self)
    self.prefs = pge_preferences.Prefs()
    self.prefs.load()

    if self.prefs.prefs_dict['auto_rotate']==True:
      self.rotation = FremantleRotation('net.khertan.pygtkeditor',self,mode=FremantleRotation.AUTOMATIC)
    else:
      self.rotation = FremantleRotation('net.khertan.pygtkeditor',self,mode=FremantleRotation.NEVER)

    self.is_fullscreen = False
    self._parent = caller

    self.set_title('PyGTKEditor')
    self.connect("key-press-event", self.on_key_press)

    menu = self.create_menu()
    menu.show_all()
    self.set_app_menu(menu)

    self.add(self._create_ui())
    self.show_all()

  def _create_ui(self):
    p1 = hildon.PannableArea()
    vbox = gtk.VBox()
    p1.add(vbox)

    vbox.add(gtk.Label('PyGTKEditor %s' % (self._parent.VERSION,)))
    i = gtk.Image()
    i.set_from_icon_name('pygtkeditor',gtk.ICON_SIZE_LARGE_TOOLBAR)
    vbox.add(i)

    hbox = gtk.HBox()
    new_button = hildon.Button(0,0)
    new_button.set_label('New')
    new_button.connect("clicked", self.menu_button_clicked, 'New')

    open_button = hildon.Button(0,0)
    open_button.set_label('Open')
    open_button.connect("clicked", self.open_dialog)

    hbox.add(new_button)
    hbox.add(open_button)
    vbox.add(hbox)

    self.recent_manager = gtk.recent_manager_get_default()
#    self.recent_manager.set_limit(3)
    self.recent_manager.connect('changed',self.recent_manager_changed)
    ritems=self.recent_manager.get_items()
    ritems.sort(lambda x,y: y.get_modified()-x.get_modified())

    if (len(ritems)>2):
      vbox.add(gtk.Label('Recent Files'))
      self.recent_button_1=hildon.Button(0,1)
      label = ritems[0].get_uri_display()
      self.recent_button_1.set_title(os.path.basename(label))
      self.recent_button_1.set_value(label)
      self.recent_button_1.set_alignment(0.0,0.0,0.0,0.5)
      vbox.add(self.recent_button_1)
      self.recent_button_1.connect("clicked", self.recent_button_clicked, label)
      self.recent_button_2=hildon.Button(0,1)
      label = ritems[1].get_uri_display()
      self.recent_button_2.set_title(os.path.basename(label))
      self.recent_button_2.set_value(label)
      self.recent_button_2.set_alignment(0.0,0.0,0.0,0.5)
      vbox.add(self.recent_button_2)
      self.recent_button_2.connect("clicked", self.recent_button_clicked, label)
      self.recent_button_3=hildon.Button(0,1)
      label = ritems[2].get_uri_display()
      self.recent_button_3.set_title(os.path.basename(label))
      self.recent_button_3.set_value(label)
      self.recent_button_3.set_alignment(0.0,0.0,0.0,0.5)
      vbox.add(self.recent_button_3)
      self.recent_button_3.connect("clicked", self.recent_button_clicked, label)

    return p1

  def recent_manager_changed(self,widget,*data):
    ritems=self.recent_manager.get_items()
    ritems.sort(lambda x,y: y.get_modified()-x.get_modified())
    if (len(ritems)>2) and (self.hasattr('recent_button_1')):
      label = ritems[0].get_uri_display()
      self.recent_button_1.set_title(os.path.basename(label))
      self.recent_button_1.set_value(label)
      label = ritems[1].get_uri_display()
      self.recent_button_2.set_title(os.path.basename(label))
      self.recent_button_2.set_value(label)
      label = ritems[2].get_uri_display()
      self.recent_button_3.set_title(os.path.basename(label))
      self.recent_button_3.set_value(label)


  def recent_button_clicked(self,button,url):
    url = button.get_value()
    self._parent.create_window(url)

  def menu_button_clicked(self,button, label):
    if label == 'New':
      self._parent.create_window()
    elif label=='Recent':
      filepath = pge_recentchooser.Dialog().get()
      if filepath!=None:
        self._parent.create_window(filepath)
#       fc = gtk.RecentChooserDialog("Recent Documents", self, None,(gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT))
#       if fc.run()==gtk.RESPONSE_ACCEPT:
#         filepath = fc.get_current_item().get_uri()[7::]
#         fc.destroy()
#         self._parent.create_window(filepath)
#       else:
#         fc.destroy()
    elif label=='About':
      self._parent.onAbout(self)
    elif label == 'Open':
      self.open_dialog()
    elif label == 'Help':
      self.show_help()
    elif label == 'Settings':
      prefs = pge_preferences.Prefs()
      prefs.load()
      prefs.edit(self)
    else:
      print "Menu Button clicked: %s" % label

  def create_menu(self):
    menu = hildon.AppMenu()
    #New
    self.new_menu_button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
    label = 'New'
    self.new_menu_button.set_label(label)
    self.new_menu_button.connect("clicked", self.menu_button_clicked, label)
    menu.append(self.new_menu_button)
    self.open_menu_button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
    label = 'Open'
    self.open_menu_button.set_label(label)
    self.open_menu_button.connect("clicked", self.menu_button_clicked, label)
    menu.append(self.open_menu_button)
    self.saveas_menu_button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
    self.recent_menu_button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
    label = 'Recent'
    self.recent_menu_button.set_label(label)
    self.recent_menu_button.connect("clicked", self.menu_button_clicked, label)
    menu.append(self.recent_menu_button)
#    label = 'Save as'
#    self.saveas_menu_button.set_label(label)
#    self.saveas_menu_button.connect("clicked", self.menu_button_clicked, label)
#    menu.append(self.saveas_menu_button)
    self.about_menu_button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
    label = 'About'
    self.about_menu_button.set_label(label)
    self.about_menu_button.connect("clicked", self.menu_button_clicked, label)
    menu.append(self.about_menu_button)
    self.settings_menu_button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
    label = 'Settings'
    self.settings_menu_button.set_label(label)
    self.settings_menu_button.connect("clicked", self.menu_button_clicked, label)
    menu.append(self.settings_menu_button)
    self.help_menu_button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
    label = 'Help'
    self.help_menu_button.set_label(label)
    self.help_menu_button.connect("clicked", self.menu_button_clicked, label)
    menu.append(self.help_menu_button)

    return menu

  def open_dialog(self,*data):
      fc = gobject.new(hildon.FileChooserDialog, action=gtk.FILE_CHOOSER_ACTION_OPEN)
      fc.set_property('show-files',True)
      fc.set_current_folder(self._parent._last_opened_folder)
      if fc.run()==gtk.RESPONSE_OK:
        filepath = fc.get_filename()
        fc.destroy()
        self._parent._last_opened_folder = os.path.dirname(filepath)
        self._parent.create_window(filepath)
      else:
        fc.destroy()

  def show_help(self):
    import pge_help
    pge_help.Help()

  def on_key_press(self, widget, event, *args):
    if (event.state==gtk.gdk.CONTROL_MASK):
      #Open : CTRL-O
      if (event.keyval == gtk.keysyms.o):
        self.open_dialog()
      #Close : CTRL-W
      elif (event.keyval == gtk.keysyms.w):
        self.destroy()
      #Show Help
      elif (event.keyval == gtk.keysyms.h):
        self.show_help()

  def apply_prefs(self,prefs=None,theme=None):
    self.prefs = prefs
    #rotate
    if self.prefs.prefs_dict['auto_rotate']==True:
      self.rotation.set_mode(FremantleRotation.AUTOMATIC)
#      FremantleRotation('net.khertan.pygtkeditor',self,mode=FremantleRotation.AUTOMATIC)
    else:
      self.rotation.set_mode(FremantleRotation.NEVER)
#      FremantleRotation('net.khertan.pygtkeditor',self,mode=FremantleRotation.NEVER)

if __name__ == "__main__":
  Window()
  gtk.main()
