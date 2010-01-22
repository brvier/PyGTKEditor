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

LANGUAGES = (('.R','R'),
            ('.ada','ada'),
            ('.c','c'),
            ('.changelog','changelog'),
            ('.cpp','cpp'),
            ('.csharp','csharp'),
            ('.desktop','desktop'),
            ('.css','css'),
            ('.diff','diff'),
            ('.fort','fortran'),
            ('.gtkrc','gtkrc'),
            ('.haskell','haskell'),
            ('.html','html'),
            ('.idl','idl'),
            ('.ini','ini'),
            ('.java','java'),
            ('.js','javascript'),
            ('.tex','latex'),
            ('.lua','lua'),
            ('makefile','makefile'),
            ('markdown','markdown'),
            ('.msil','msil'),
            ('nemerle','nemerle'),
            ('octave','octave'),
            ('.pas','pascal'),
            ('.pl','perl'),
            ('.php','php'),
            ('.po','po'),
            ('.py','python'),
            ('.rb','ruby'),
            ('.scheme','scheme'),
            ('.sh','sh'),
            ('.tcl','tcl'),
            ('texinfo','texinfo'),
            ('.txt','None'),
            ('.vb','vbnet'),
            ('verilog','verilog'),
            ('vhdl','vhdl'),
            ('.xml','xml'),
            )

class Window(hildon.Window):
  def __init__(self,filepath=None,caller=None):
    hildon.Window.__init__ (self)
    self.prefs = pge_preferences.Prefs()
    self.prefs.load()

    if self.prefs.prefs_dict['auto_rotate']==True:
      self.rotation = FremantleRotation('net.khertan.pygtkeditor',self,mode=FremantleRotation.AUTOMATIC)
    else:
      self.rotation = FremantleRotation('net.khertan.pygtkeditor',self,mode=FremantleRotation.NEVER)
    
    self.is_fullscreen = False
    
    self._parent = caller
    self.filepath=filepath

    self.code_editor=pge_editor.Editor(self._detect_language(self.filepath),font_name=self.prefs.prefs_dict['font_name'],font_size=self.prefs.prefs_dict['font_size'])

    self.toolbar = self.create_toolbar()
    self.add_toolbar(self.toolbar)

    menu = self.create_menu()
    menu.show_all()
    self.set_app_menu(menu)
    
    self.create_findtoolbar()

    p1 = hildon.PannableArea()
    p1.set_property('mov_mode',hildon.MOVEMENT_MODE_BOTH)

    p1.add(self.code_editor)

    #self.code_editor
    self.add(p1)
    self.show_all()
    self.saved=True

    print filepath
    if filepath!=None:
      self.set_title(os.path.basename(filepath))
      self.open_file(filepath)
    else:
      self.set_title('Untitled')

    self.connect("key-press-event", self.on_key_press)
    self.code_editor.buffer.connect ('changed', self.on_modified)

    #self.app.add_window(self)

  def create_findtoolbar(self):
    self.findToolBar = hildon.FindToolbar("Search for :")
    self.add_toolbar(self.findToolBar)

    self.findToolBar.connect("close", self.onHideFind)
    self.findToolBar.connect("search", self.onSearchFind)
    self.findToolBar.set_no_show_all(True)

  def onShowFind(self, widget):
    self.findToolBar.show()
    for fchild in self.findToolBar.get_children():
      try:
        for achild in fchild.get_children():
          try:
            for cchild in achild.get_children():
              if type(cchild)==gtk.ComboBoxEntry:
                self.set_focus(cchild.get_children()[0])                 
          except:
            pass
      except:
        pass

  def apply_prefs(self):
    self.prefs.load()
    #rotate
    if self.prefs.prefs_dict['auto_rotate']==True:
      self.rotation.set_mode(FremantleRotation.AUTOMATIC)
#      FremantleRotation('net.khertan.pygtkeditor',self,mode=FremantleRotation.AUTOMATIC)
    else:
      self.rotation.set_mode(FremantleRotation.NEVER)
#      FremantleRotation('net.khertan.pygtkeditor',self,mode=FremantleRotation.NEVER)
    #font / size
    print self.prefs.prefs_dict['font_name']+" "+str(self.prefs.prefs_dict['font_size'])
    self.code_editor.modify_font(pango.FontDescription (self.prefs.prefs_dict['font_name']+" "+str(self.prefs.prefs_dict['font_size'])))
    
    if self.prefs.prefs_dict['show_lines'] == True:
      self.code_editor.set_border_window_size(gtk.TEXT_WINDOW_LEFT, 30)
      self.code_editor.line_view = self.code_editor.get_window(gtk.TEXT_WINDOW_LEFT)
      if self.code_editor.expose_event_cb==None:
        self.code_editor.expose_even_cb = self.code_editor.connect("expose_event", self.code_editor.line_numbers_expose)
    else:
      self.code_editor.set_border_window_size(gtk.TEXT_WINDOW_LEFT, 0)
#      self.code_editor.line_view = None
      if self.code_editor.expose_event_cb!=None:
        self.code_editor.disconnect(self.code_editor.expose_event_cb)
  
  def onHideFind(self, widget):
    self.findToolBar.hide()
    self.searched_text = None

  def onSearchFind(self,widget,data=None):
    text = widget.get_property("prefix")
    self.code_editor.search(text)

  def on_modified(self,buf,data=None):
    self.saved=False
    title = self.get_title()
    if title.startswith('*'):
      return
    else:
      self.set_title('*'+title)
       
  def execute(self):
    note = osso.SystemNote(self._parent.context)
    result = note.system_note_infoprint("Launching "+ self.filepath +" ...")

    fileHandle = open('/tmp/pygtkeditor.tmp', 'w')
    fileHandle.write('#!/bin/sh\n')
    fileHandle.write('cd '+os.path.dirname(self.filepath)+' \n')
    fileHandle.write(self._detect_launch_language()+" \'"+self.filepath + "\'\n")
    fileHandle.write('read -p "Press ENTER to continue ..." foo')
    fileHandle.write('\nexit')
    fileHandle.close()
    commands.getoutput("chmod 777 /tmp/pygtkeditor.tmp")
    Popen('/usr/bin/osso-xterm /tmp/pygtkeditor.tmp',shell=True,stdout=None)

  def _detect_launch_language(self):
    return 'python'
    
  def _detect_language(self,filepath):
        
    if filepath==None:
      return self.prefs.prefs_dict['default_language']
                  
    for extension,lang in LANGUAGES:
      if filepath.endswith(extension.lower()):
        return lang
    return self.prefs.prefs_dict['default_language']

  def on_key_press(self, widget, event, *args):
    if (event.state==gtk.gdk.CONTROL_MASK):
      #Save : CTRL-S
      if (event.keyval == gtk.keysyms.s):
        self.save(self.filepath)
      #Undo : CTRL-Z
      elif (event.keyval == gtk.keysyms.z):
        self.code_editor.buffer.undo()
      #Redo : CTRL-Y
      elif (event.keyval == gtk.keysyms.y):
        self.code_editor.buffer.redo()
      #Open : CTRL-O
      elif (event.keyval == gtk.keysyms.o):
        self.open_dialog()
      #Searh : CTRL-F
      elif (event.keyval == gtk.keysyms.f):
        self.onShowFind(widget) 
      #Duplicate line : CTRL-D
      elif (event.keyval == gtk.keysyms.d):
        self.code_editor.duplicate_line() 
      #Close : CTRL-W
      elif (event.keyval == gtk.keysyms.w):
        self.destroy() 
      #Show Info : CTRL-I
      elif (event.keyval == gtk.keysyms.i):
        info = hildon.FileDetailsDialog(self,self.filepath)
        info.run()
        info.destroy()
      #Show Help
      elif (event.keyval == gtk.keysyms.h):
        self.show_help()
      #Execute
      elif (event.keyval == gtk.keysyms.e):
        self.execute()

  def show_help(self):
    import pge_help
    pge_help.Help()

  def save_file(self,filepath):
    try:
      f = open(filepath,'w')
      buf = self.code_editor.get_buffer()
      start,end = buf.get_bounds()
      f.write(buf.get_text(start,end))
      f.close()
      self.set_title(os.path.basename(filepath))
      self.saved=True
      self.filepath = filepath
      note = osso.SystemNote(self._parent.context)
      result = note.system_note_infoprint(self.filepath+' Saved')
      language = self._detect_language(self.filepath)
      if self.code_editor.language != language:
        self.code_editor.reset_language(language)
    except StandardError,e:
      note = osso.SystemNote(self._parent.context)
      result = note.system_note_dialog('An error occurs saving file :\n'+str(e))

  def open_dialog(self):
      #fsm = hildon.FileSystemModel()
      #fsm.set_property('visible-columns',7)
      #fc =hildon.FileChooserDialog(self, gtk.FILE_CHOOSER_ACTION_OPEN,fsm)
      fc = gobject.new(hildon.FileChooserDialog, action=gtk.FILE_CHOOSER_ACTION_OPEN)
      fc.set_property('show-files',True)
      fc.set_current_folder(self._parent._last_opened_folder)
      #fsm.set_property('visible-columns',7)
      #fc.set_extension('py')
      if fc.run()==gtk.RESPONSE_OK:
        filepath = fc.get_filename()
        fc.destroy()
        self._parent._last_opened_folder = os.path.dirname(filepath)
        self._parent.create_window(filepath)
      else:
        fc.destroy()

  def save_as(self):
    fsm = hildon.FileSystemModel()
#    fc = hildon.FileChooserDialog(self, gtk.FILE_CHOOSER_ACTION_SAVE,fsm)
    fc = gobject.new(hildon.FileChooserDialog, action=gtk.FILE_CHOOSER_ACTION_SAVE)      
    if self.filepath != None :
      fc.set_current_folder(os.path.dirname(self.filepath))
    else: 
      fc.set_current_folder(self._parent._last_opened_folder)
    fc.set_show_hidden(True)
    fc.set_do_overwrite_confirmation(False)

    fp = self.filepath
    if fp == None:
      fp = 'Untitled'
    self.set_title(os.path.basename(fp))
    self._parent._last_opened_folder = os.path.dirname(fp)
    fc.set_property('autonaming',False)
    fc.set_property('show-files',True)
#    fc.set_current_folder(os.path.dirname(fp))
    fc.set_current_name(os.path.basename(fp))
#    fc.set_extension('py')
    if fc.run()==gtk.RESPONSE_OK:
      filepath = fc.get_filename()
      fc.destroy()
      self.save_file(filepath)
      manager = gtk.recent_manager_get_default()                         
      manager.add_item('file://'+filepath)                               
    else:
      fc.destroy()

  def open_file(self,filepath):
    try:
      f = open(filepath,'r')
      self.filepath = os.path.abspath(filepath)
      buf = self.code_editor.get_buffer()
      buf.begin_user_action()
      text = f.read()
      f.close()
      buf.begin_not_undoable_action()
      text=text.encode('UTF-8')
      buf.set_text(text)
      buf.end_not_undoable_action()
      buf.end_user_action()
      manager = gtk.recent_manager_get_default()
      manager.add_item('file://'+filepath)
    except StandardError,e:
      print e
      note = osso.SystemNote(self._parent.context)
      result = note.system_note_dialog('An error occurs opening file :\n'+str(e))
  
  def create_toolbar(self):
    toolbar = gtk.Toolbar()
#    label = 'Edit'
#    pbuf = gtk.IconTheme().load_icon('browser_panning_mode_off',gtk.ICON_SIZE_BUTTON,gtk.ICON_LOOKUP_USE_BUILTIN)
#    i = gtk.Image()
#    i.set_from_pixbuf(pbuf)
#
#    toolitem = gtk.ToggleToolButton()
#    toolitem.set_icon_widget(i)
#    toolitem.connect("toggled", self.toolbar_button_clicked, label)    
#    toolbar.insert(toolitem, 0)

    label = 'Comment'
    toolitem = gtk.ToolButton(gtk.image_new_from_stock(gtk.STOCK_UNDERLINE,
                                 gtk.ICON_SIZE_LARGE_TOOLBAR),
                                 label)
    toolitem.connect("clicked", self.toolbar_button_clicked, label)
    toolbar.insert(toolitem, 0)

    label = 'Indent'
    toolitem = gtk.ToolButton(gtk.image_new_from_stock(gtk.STOCK_INDENT,
                                 gtk.ICON_SIZE_LARGE_TOOLBAR),
                                 label)
    toolitem.connect("clicked", self.toolbar_button_clicked, label)
    toolbar.insert(toolitem, 1)

    label = 'Unindent' 
    toolitem = gtk.ToolButton(gtk.image_new_from_stock(gtk.STOCK_UNINDENT,
                                 gtk.ICON_SIZE_LARGE_TOOLBAR),
                                 label)
    toolitem.connect("clicked", self.toolbar_button_clicked, label)    
    toolbar.insert(toolitem, 2)

    toolbar.insert(gtk.SeparatorToolItem(),3)

    label = 'Save'
    toolitem = gtk.ToolButton(gtk.image_new_from_stock(gtk.STOCK_SAVE,
                                 gtk.ICON_SIZE_LARGE_TOOLBAR),
                                 label)
    toolitem.connect("clicked", self.toolbar_button_clicked, label)    
    toolbar.insert(toolitem, 4)

    toolbar.insert(gtk.SeparatorToolItem(),5)

    label = 'Search'
    toolitem = gtk.ToolButton(gtk.image_new_from_stock(gtk.STOCK_FIND,
                                 gtk.ICON_SIZE_LARGE_TOOLBAR),
                                 label)
    toolitem.connect("clicked", self.toolbar_button_clicked, label)    
    toolbar.insert(toolitem, 6)

    label = 'Fullscreen'
    toolitem = gtk.ToolButton(gtk.image_new_from_stock(gtk.STOCK_FULLSCREEN,
                                 gtk.ICON_SIZE_LARGE_TOOLBAR),
                                 label)
    toolitem.connect("clicked", self.toolbar_button_clicked, label)    
    toolbar.insert(toolitem, 7)

    toolbar.insert(gtk.SeparatorToolItem(),8)

    label = 'Execute'
    toolitem = gtk.ToolButton(gtk.image_new_from_stock(gtk.STOCK_EXECUTE,
                                 gtk.ICON_SIZE_LARGE_TOOLBAR),
                                 label)
    toolitem.connect("clicked", self.toolbar_button_clicked, label)    
    toolbar.insert(toolitem, 9)

    return toolbar

  def save(self):
    if self.filepath!=None:
      self.save_file(self.filepath)
    else:
      self.save_as()

  def toolbar_button_clicked (self,toolbutton, label):
    print "Toolbar button clicked : %s" % label
    if label=='Save':
      self.save()
    elif label=='Indent':
      self.code_editor.indent_tab()
    elif label=='Comment':
      self.code_editor.comment_text()
    elif label=='Unindent':
      self.code_editor.unindent_tab()
    elif label=='Search':
      self.onShowFind(toolbutton) 
    elif label=='Fullscreen':
      self.is_fullscreen = not self.is_fullscreen
      if self.is_fullscreen==True:
        self.fullscreen()
      else:
        self.unfullscreen()
    elif label=='Execute':
      self.execute()
      
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
    elif label == 'Save as':
      self.save_as()
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
    label = 'Save as'
    self.saveas_menu_button.set_label(label)
    self.saveas_menu_button.connect("clicked", self.menu_button_clicked, label)
    menu.append(self.saveas_menu_button)
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
