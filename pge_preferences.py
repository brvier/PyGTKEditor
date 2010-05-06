import hildon
import gtk
import pge_window
import cPickle
import pge_window
import os

class Prefs():
  def __init__(self):
    self.prefs_dict = {}

  def load(self):
    try:
      f = open(os.path.expanduser("~")+"/.pygtkeditor",'r')
      self.prefs_dict = cPickle.load(f)
      if not self.prefs_dict.has_key('auto_rotate'):
        self.prefs_dict['auto_rotate']=True
      if not self.prefs_dict.has_key('show_lines'):
        self.prefs_dict['show_lines']=False
      if not self.prefs_dict.has_key('indent'):
        self.prefs_dict['indent']='  '
      if not self.prefs_dict.has_key('auto_clean_line_end'):
        self.prefs_dict['auto_clean_line_end']=False
      if not self.prefs_dict.has_key('theme'):
        self.prefs_dict['theme']='default'

    except:
      self.default()

  def default(self):
    self.prefs_dict['hildon_text_completion']=True
    self.prefs_dict['default_language']='python'
    self.prefs_dict['font_name']='Monospace'
    self.prefs_dict['font_size']='12'
    self.prefs_dict['auto_rotate']=True
    self.prefs_dict['show_lines']=False
    self.prefs_dict['indent']='  '
    self.prefs_dict['auto_clean_line_end']=False

  def store(self):
    f = open(os.path.expanduser("~")+"/.pygtkeditor",'w')
    prefs = cPickle.dump(self.prefs_dict,f)

  def edit(self,parent_window):
    dialog = gtk.Dialog('PyGTKEditor - Settings',parent_window,gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_OK,gtk.RESPONSE_ACCEPT))

    #hildon_text_completion
    w_hildon_text_completion = hildon.CheckButton(gtk.HILDON_SIZE_AUTO)
    w_hildon_text_completion.set_label('Hildon Text Completion')
    if self.prefs_dict.has_key('hildon_text_completion'):
      w_hildon_text_completion.set_active((self.prefs_dict['hildon_text_completion']==True))

    #show lines numbers
    w_show_lines = hildon.CheckButton(gtk.HILDON_SIZE_AUTO)
    w_show_lines.set_label('Show lines numbers')
    if self.prefs_dict.has_key('show_lines'):
      w_show_lines.set_active((self.prefs_dict['show_lines']==True))

    #auto clean line end
    w_auto_clean_line_end = hildon.CheckButton(gtk.HILDON_SIZE_AUTO)
    w_auto_clean_line_end.set_label('Auto clean line end (on save)')
    if self.prefs_dict.has_key('auto_clean_line_end'):
      w_auto_clean_line_end.set_active((self.prefs_dict['auto_clean_line_end']==True))

    #auto_rotate
    w_auto_rotate = hildon.CheckButton(gtk.HILDON_SIZE_AUTO)
    w_auto_rotate.set_label('Auto Portrait Mode')
    if self.prefs_dict.has_key('auto_rotate'):
      w_auto_rotate.set_active((self.prefs_dict['auto_rotate']==True))

    #default_language
    w_default_language = hildon.PickerButton(gtk.HILDON_SIZE_AUTO,
                                       hildon.BUTTON_ARRANGEMENT_VERTICAL)
    w_default_language.set_title("Default Language")
    w_default_language_selector = hildon.TouchSelectorEntry(text=True)
    languages = ['None']
    print self.prefs_dict['default_language']
    for ext,language in pge_window.LANGUAGES:
      languages.append(language)
    for language in languages:
      w_default_language_selector.append_text(language)
    w_default_language.set_selector(w_default_language_selector)
    if self.prefs_dict.has_key('default_language'):
      w_default_language.set_active(languages.index(self.prefs_dict['default_language']))

    #Font Button
    w_font = hildon.PickerButton(gtk.HILDON_SIZE_AUTO,
                                       hildon.BUTTON_ARRANGEMENT_VERTICAL)
    w_font.set_title("Font")
    w_font_selector = hildon.TouchSelectorEntry(text=True)
    c = parent_window.create_pango_context()
    families = c.list_families()
    font_names = []
    for f in families:
      font_names.append(f.get_name())
    for f in font_names:
      w_font_selector.append_text(f)
    w_font.set_selector(w_font_selector)
    if self.prefs_dict.has_key('font_name'):
      w_font.set_active(font_names.index(self.prefs_dict['font_name']))
      w_font.set_value(self.prefs_dict['font_name'])

    #Font Size Button
    w_font_size = hildon.PickerButton(gtk.HILDON_SIZE_AUTO,
                                       hildon.BUTTON_ARRANGEMENT_VERTICAL)
    w_font_size.set_title("Size")
    w_font_size_selector = hildon.TouchSelectorEntry(text=True)
    font_sizes = []
    for f in range(7,49):
      font_sizes.append(str(f))
    for f in font_sizes:
      w_font_size_selector.append_text(f)
    w_font_size.set_selector(w_font_size_selector)
    if self.prefs_dict.has_key('font_size'):
      w_font_size.set_active(font_sizes.index(self.prefs_dict['font_size']))
      w_font_size.set_value(self.prefs_dict['font_size'])

    #Indent Button
    w_indent = hildon.PickerButton(gtk.HILDON_SIZE_AUTO,
                                       hildon.BUTTON_ARRANGEMENT_VERTICAL)
    w_indent.set_title("Indent Style")
    w_indent_selector = hildon.TouchSelectorEntry(text=True)
    indent_style = ['2 spaces','4 spaces','Tabulation']
    indent_value = ['  ','    ','\t']
    for i in range(3):
      w_indent_selector.append_text(indent_style[i])
    w_indent.set_selector(w_indent_selector)
    if self.prefs_dict.has_key('indent'):
      print self.prefs_dict['indent']
      w_indent.set_active(indent_value.index(self.prefs_dict['indent']))
      w_indent.set_value(indent_style[indent_value.index(self.prefs_dict['indent'])])
    else:
      w_indent.set_active(0)
      w_indent.set_value(indent_style[0])

    #Theme Button
    w_theme = hildon.PickerButton(gtk.HILDON_SIZE_AUTO,
                                       hildon.BUTTON_ARRANGEMENT_VERTICAL)
    w_theme.set_title("Syntax Hilight Theme")
    w_theme_selector = hildon.TouchSelectorEntry(text=True)
    theme_list = ['default','dark',]
    for i in theme_list :
      w_theme_selector.append_text(i)
    w_theme.set_selector(w_theme_selector)
    if self.prefs_dict.has_key('theme'):
      w_theme.set_active(theme_list.index(self.prefs_dict['theme']))
      w_theme.set_value(self.prefs_dict['theme'])
    else:
      w_theme.set_active(0)
      w_theme.set_value(theme_list[0])

    p2 = hildon.PannableArea()
    p = gtk.VBox()
#    dialog.vbox.add(w_hildon_text_completion)
#    dialog.vbox.add(w_show_lines)
#    dialog.vbox.add(w_auto_rotate)
#    dialog.vbox.add(w_default_language)
#    hbox = gtk.HBox()
#    hbox.add(w_font)
#    hbox.add(w_font_size)
#    dialog.vbox.add(hbox)
#    dialog.vbox.add(w_indent)
#    dialog.vbox.add(w_auto_clean_line_end)
    p.add(w_hildon_text_completion)
    p.add(w_show_lines)
    p.add(w_auto_rotate)
    p.add(w_default_language)
    hbox = gtk.HBox()
    hbox.add(w_font)
    hbox.add(w_font_size)
    p.add(hbox)
    p.add(w_indent)
    p.add(w_auto_clean_line_end)
    p.add(w_theme)
    p2.set_size_request(-1,300)
    p2.add_with_viewport(p)
    dialog.vbox.add(p2)
#    p1 = hildon.PannableArea()
    #p1.set_size_request(600,400)
#    p1.add(vbox)
#    dialog.get_child().get_child().add(p1)
#    dialog.vbox.add(p1)
    dialog.show_all()
    if(dialog.run()==gtk.RESPONSE_ACCEPT):
      self.prefs_dict['hildon_text_completion']=w_hildon_text_completion.get_active()
      self.prefs_dict['auto_rotate']=w_auto_rotate.get_active()
      self.prefs_dict['show_lines']=w_show_lines.get_active()
      self.prefs_dict['default_language']= w_default_language_selector.get_current_text()
      self.prefs_dict['font_name']= w_font_selector.get_current_text()
      self.prefs_dict['font_size']= w_font_size_selector.get_current_text()
      self.prefs_dict['indent']= indent_value[w_indent_selector.get_active(0)]
      self.prefs_dict['auto_clean_line_end']=w_auto_clean_line_end.get_active()
      self.prefs_dict['theme']= w_theme_selector.get_current_text()
      self.store()
      parent_window._parent.apply_prefs()
    dialog.destroy()

if __name__ == "__main__":
  prefs = Prefs()
  prefs.load()
  prefs.edit(hildon.Window())