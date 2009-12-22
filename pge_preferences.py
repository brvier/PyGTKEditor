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
    except:
      self.default()
      
  def default(self):
    self.prefs_dict['hildon_text_completion']=True
    self.prefs_dict['default_language']='python'     

  def store(self):
    f = open(os.path.expanduser("~")+"/.pygtkeditor",'w')
    prefs = cPickle.dump(self.prefs_dict,f)

  def edit(self,parent_window):
    dialog = gtk.Dialog('Preferences',parent_window,gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_OK,gtk.RESPONSE_ACCEPT))
#    dialog = hildon.PickerDialog(parent_window)
    #hildon_text_completion
    w_hildon_text_completion = hildon.CheckButton(gtk.HILDON_SIZE_AUTO)
    w_hildon_text_completion.set_label('Hildon Text Completion')
    if self.prefs_dict.has_key('hildon_text_completion'):
      w_hildon_text_completion.set_active((self.prefs_dict['hildon_text_completion']==True))

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
    
#    vbox = gtk.VBox()
    
    dialog.vbox.add(w_hildon_text_completion)
    dialog.vbox.add(w_default_language)
    p1 = hildon.PannableArea()
    #p1.set_size_request(600,400)
#    p1.add(vbox)
#    dialog.get_child().get_child().add(p1)
#    dialog.vbox.add(p1)
    dialog.show_all()
    if(dialog.run()==gtk.RESPONSE_ACCEPT):
      self.prefs_dict['hildon_text_completion']=w_hildon_text_completion.get_active()
      self.prefs_dict['default_language']= w_default_language_selector.get_current_text()
      self.store()
    dialog.destroy()
    
if __name__ == "__main__":
  prefs = Prefs()
  prefs.load()
  prefs.edit(hildon.Window())
