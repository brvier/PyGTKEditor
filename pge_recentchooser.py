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

class Dialog(hildon.Dialog):
  def __init__(self):
    hildon.Dialog.__init__ (self)
    self.set_title('Choose a file to open')
    self.selected = None
    
    vbox = gtk.VBox()
    p1 = hildon.PannableArea()
    p1.add_with_viewport(vbox)
    
    rm = gtk.recent_manager_get_default()
    ritems = rm.get_items()
    ritems.sort(lambda x,y: y.get_modified()-x.get_modified())

    if (len(ritems)>0):
#      vbox.add(gtk.Label('Recent Files'))        

      for index,item in enumerate(ritems):
        b=hildon.Button(0,1)
        label = item.get_uri_display()
        i = gtk.image_new_from_stock(gtk.STOCK_FILE,gtk.ICON_SIZE_BUTTON)
#        i = gtk.image_new_from_icon_name(item.get_mime_type(),gtk.ICON_SIZE_BUTTON)
#        i = gtk.image_new_from_pixbuf(item.get_icon(gtk.ICON_SIZE_LARGE_TOOLBAR))
        b.set_image(i)
        b.set_title(os.path.basename(label))
        b.set_value(label)
        b.set_alignment(0.0,0.0,0.0,0.5)
        vbox.add(b)
        b.connect("clicked", self._clicked, label)
    
#    vbox
    p1.set_size_request(-1,350)
    self.vbox.add(p1)
    self.vbox.show_all()

  def _clicked(self,w,label):
    self.selected = label
    self.destroy()
    
  def get(self):
    self.run()
    return self.selected
    
if __name__ == "__main__":
  print Dialog().get()
  gtk.main()
