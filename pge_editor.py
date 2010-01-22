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

import sys
import hildon
import gtk
#import gtk.glade
import osso
import pango
import threading
import re
import os.path
import commands
import cPickle
from subprocess import *
from pge_buffer import SyntaxLoader,CodeBuffer
import pge_preferences 

###############################################################################
# @brief Code editor widget
###############################################################################
class Editor (hildon.TextView):

  #############################################################################
  # @brief Initialize CodeEditor
  #############################################################################
  def __init__ (self,language=None,font_name='Monospace',font_size='11'):

#    self.language_manager=gtksourceview2.LanguageManager()
    if (language != None) and (language != 'None'):
      lang = SyntaxLoader(language)
    else:
      lang = None
    self.buffer=CodeBuffer(lang=lang)
    hildon.TextView.__init__ (self)
    self.set_buffer(self.buffer)
    
    prefs = pge_preferences.Prefs()
    prefs.load()
    if prefs.prefs_dict['hildon_text_completion']==False:
      self.set_property('hildon-input-mode', gtk.HILDON_GTK_INPUT_MODE_FULL)

    self.indent = prefs.prefs_dict['indent']
    
    self.set_editable (True)
    self.no_edit_mode = True
    self.modify_font (pango.FontDescription (font_name+" "+str(font_size)))
    self.language = language
    self.searched_text = None
    self.expose_event_cb = None
    
    if prefs.prefs_dict['show_lines'] == True:
      self.set_border_window_size(gtk.TEXT_WINDOW_LEFT, 30)
      self.line_view = self.get_window(gtk.TEXT_WINDOW_LEFT)
      self.expose_event_cb = self.connect("expose_event", self.line_numbers_expose)
  
#  def on_key_press(self, widget, event, *args):
#    #CTRL-S : save
#    if (event.keyval == gtk.keysyms.s) and (event.state==gtk.gdk.CONTROL_MASK):
#      self.save(self.filepath)

  def get_lines(self, first_y, last_y, buffer_coords, numbers):
    text_view = self
    # Get iter at first y
    iter, top = text_view.get_line_at_y(first_y)

    # For each iter, get its location and add it to the arrays.
    # Stop when we pass last_y
    count = 0
    size = 0

    while not iter.is_end():
      y, height = text_view.get_line_yrange(iter)
      buffer_coords.append(y)
      line_num = iter.get_line()
      numbers.append(line_num)
      count += 1
      if (y + height) >= last_y:
        break
      iter.forward_line()

    return count
      
  def line_numbers_expose(self, widget, event, user_data=None):
    text_view = widget

    type = gtk.TEXT_WINDOW_LEFT
    target = text_view.get_window(gtk.TEXT_WINDOW_LEFT)
    target.set_background(gtk.gdk.Color(0,0,60000))
 
    first_y = event.area.y
    last_y = first_y + event.area.height

    x, first_y = text_view.window_to_buffer_coords(type, 0, first_y)
    x, last_y = text_view.window_to_buffer_coords(type, 0, last_y)

    numbers = []
    pixels = []
    count = self.get_lines(first_y, last_y, pixels, numbers)
    # Draw fully internationalized numbers!
    layout = widget.create_pango_layout("")

    for i in range(count):
        x, pos = text_view.buffer_to_window_coords(type, 0, pixels[i])
        str = '%d' % numbers[i]
        layout.set_text(str)
        widget.style.paint_layout(target, widget.state, False,
                                  None, widget, None, 2, pos + 2, layout)

    # don't stop emission, need to draw children
    return False

  def reset_language(self,language):
    if (language == 'None'):
      language=None
    self.language = language
    lang = SyntaxLoader(self.language)
    self.buffer.reset_language(lang)

  #############################################################################
  # @brief Selectable ?
  #############################################################################
  def selectable(self,widget,event,*data):
    return self.no_edit_mode

  #############################################################################
  # @brief Increase font size
  #############################################################################
  def increase_font_size(self):
    self.font_size=self.font_size+1
    self.modify_font (pango.FontDescription ("Monospace "+str(self.font_size)))

  #############################################################################
  # @brief Undo
  #############################################################################
  def undo(self):
    self.buffer.undo()

  #############################################################################
  # @brief Redo
  #############################################################################
  def redo(self):
    self.buffer.redo()

  #############################################################################
  # @brief Decrease font size
  #############################################################################
  def decrease_font_size(self):
    self.font_size=self.font_size-1
    self.modify_font (pango.FontDescription ("Monospace "+str(self.font_size)))

  #############################################################################

#  def set_language(self,language):
#    self.__language=language
#    self.buffer.set_language(self.language_manager.get_language(language))
#    self.set_indent_width(2)
#    self.set_auto_indent(True)
#    self.set_tab_width(2)
#    self.set_insert_spaces_instead_of_tabs(True)
#    self.set_indent_on_tab(True)
#    self.set_show_line_numbers(True)

  #############################################################################
  # @brief Find a substring
  #############################################################################
  def search(self,text):
    buffer = self.buffer
    if self.searched_text != text:
      self.searched_text = text
      self.searched_text_count = 0

      start, end = buffer.get_bounds ()
      
      buffer.remove_tag_by_name('search_hilight',start,end)

      self.search_results_list=[]

      search_results = self.findSubstring(buffer.get_text (start, end), text)
      buffer._apply_tags = True
      for index in search_results:
        found_start = buffer.get_iter_at_offset (index.span()[0])
        found_end   = buffer.get_iter_at_offset (index.span()[1])
        buffer.apply_tag_by_name ("search_hilight", found_start, found_end)
        self.search_results_list.append(found_start.get_offset())
      buffer._apply_tags = False
        
    else:
      self.searched_text_count =  self.searched_text_count + 1
    try:
      iter = buffer.get_iter_at_offset(self.search_results_list[self.searched_text_count])
      buffer.place_cursor(iter)
      self.scroll_to_iter(iter,0)
    except IndexError:
      note = osso.SystemNote(self.get_parent().get_parent()._parent.context)
      result = note.system_note_infoprint("End text reached")
      self.searched_text_count = -1
      


  #############################################################################
  # @brief Find a substring
  #############################################################################
  def findSubstring(self,text, substring):
    searched_text=re.compile(substring)
    return searched_text.finditer(text.decode('UTF-8'))

  #############################################################################
  # @brief Clean useless space
  #############################################################################
  def clean_space(self):
      buffer = self.get_buffer()
      offset = buffer.get_iter_at_mark(buffer.get_insert()).get_offset()
      start, end = buffer.get_bounds ()
      buffer.set_text(re.sub('\n\s+\n','\n\n',buffer.get_text(start,end)))
      buffer.place_cursor(buffer.get_iter_at_offset(offset))

  #############################################################################
  # @brief Replace tabulation
  #############################################################################
  def replace_tabs (self):
    buffer = self.get_buffer()
    tabul=' ' * 2
    start,end=buffer.get_bounds()
    text = buffer.get_text(start,end)
    text = text.replace('\t',tabul)
    buffer.set_text(text)

  #############################################################################
  # @brief DUPLICATE Line
  #############################################################################
  def duplicate_line (self):
    buffer = self.get_buffer()

    if (buffer.get_selection_bounds()!=()):
      start,end=buffer.get_selection_bounds()
      for line in range(start.get_line(),end.get_line()+1):
        text = buffer.get_text(buffer.get_iter_at_line(line),buffer.get_iter_at_line(line+1))
        buffer.insert(buffer.get_iter_at_line(line),text)
    else:
      insert = buffer.get_iter_at_mark(buffer.get_insert())
      start = buffer.get_iter_at_line(insert.get_line())
      end = buffer.get_iter_at_line(insert.get_line()+1)
      text = ''
      if start.get_line() == end.get_line():
        _,end = buffer.get_bounds()
        text = '\n'
      text = text+buffer.get_text(start,end)
      buffer.insert(buffer.get_iter_at_line(insert.get_line()),text)

  #############################################################################
  # @brief Insert tabulation
  #############################################################################
  def indent_tab (self):
    buffer = self.get_buffer()
    tabul=self.indent
    if (buffer.get_selection_bounds()!=()):
      start,end=buffer.get_selection_bounds()
      for line in range(start.get_line(),end.get_line()+1):
        buffer.insert(buffer.get_iter_at_line(line),tabul)
    else:
      buffer.insert(buffer.get_iter_at_line(buffer.get_iter_at_mark(buffer.get_insert()).get_line()),tabul)

  #############################################################################
  # @brief Unindent tabulation
  #############################################################################
  def unindent_tab (self):
    buffer = self.get_buffer()
    if (buffer.get_selection_bounds()!=()):
      start,end=buffer.get_selection_bounds()
      for line in range(start.get_line(),end.get_line()+1):
        r = buffer.get_iter_at_line(line)
        c = buffer.get_text(r,r)
        if c == '\t':
          buffer.delete(r,r)
        else:
          e=buffer.get_iter_at_offset(r.get_offset()+ len(self.indent))
          if (buffer.get_text(r,e)==self.indent):
            buffer.delete(r,e)
    else:
      r = buffer.get_iter_at_line(buffer.get_iter_at_mark(buffer.get_insert()).get_line())
      c = buffer.get_text(r,r)
      if c == '\t':
        buffer.delete(r,r)
      else:
        e=buffer.get_iter_at_offset(r.get_offset()+ len(self.indent))
        if (buffer.get_text(r,e)==self.indent):
          buffer.delete(r,e)

  #############################################################################
  # @brief Comment string
  #############################################################################
  def get_comment_string(self):
    if self.language=='cpp':
      return '//'
    if self.language=='php':
      return '//'
    elif self.language=='python':
      return '#'
    elif self.language=='sql':
      return '--'
    else:
      return '//'

  #############################################################################
  # @brief Comment / Uncomment
  #############################################################################
  def comment_text (self):
    ctext = self.get_comment_string()
    if ctext != '':
      comment = True
      buffer = self.get_buffer()
      r = buffer.get_iter_at_line(buffer.get_iter_at_mark(buffer.get_insert()).get_line()) 
      e=buffer.get_iter_at_offset(r.get_offset()+ len(ctext))
      if (buffer.get_text(r,e)==ctext): 
        comment=False
      if comment==True:
        if (buffer.get_selection_bounds()!=()):
          start,end=buffer.get_selection_bounds()
          for line in range(start.get_line(),end.get_line()+1):
            buffer.insert(buffer.get_iter_at_line(line),ctext)
        else:
          buffer.insert(buffer.get_iter_at_line(buffer.get_iter_at_mark(buffer.get_insert()).get_line()),ctext)
      else:
         if (buffer.get_selection_bounds()!=()):
           start,end=buffer.get_selection_bounds()
           for line in range(start.get_line(),end.get_line()+1):
             r = buffer.get_iter_at_line(line)
             e=buffer.get_iter_at_offset(r.get_offset()+ len(ctext))
             if (buffer.get_text(r,e) == ctext):
               buffer.delete(r,e)
         else:
           r = buffer.get_iter_at_line(buffer.get_iter_at_mark(buffer.get_insert()).get_line())
           e=buffer.get_iter_at_offset(r.get_offset()+ len(ctext))
           if (buffer.get_text(r,e) == ctext):
             buffer.delete(r,e)

