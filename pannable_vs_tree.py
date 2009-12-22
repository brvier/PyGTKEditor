import hildon
import gtk
import gobject
import pango

class Test(hildon.Window):
  def create_treeview(self):
    #Store = uid , checkbox , markup
    self.todosStore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_BOOLEAN,gobject.TYPE_STRING)
    self.todosTree=gtk.TreeView()
    self.todosTree.set_grid_lines(False)
    self.todosTree.set_fixed_height_mode(True)
    self.todosTree.set_hadjustment(gtk.Adjustment(value=0))
    self.todosTree.connect('row_activated',self.edit)
  
    checkboxrenderer = gtk.CellRendererToggle()
    checkboxrenderer.set_property('activatable' , True)
    checkboxrenderer.set_property('height' , 80)
    checkboxrenderer.set_property('width' , 60)
    checkboxrenderer.connect("toggled", self.edited_checkbox, (self.todosStore, 1))    
    column_status = gtk.TreeViewColumn("Status", checkboxrenderer, active=1)
    column_status.set_spacing(0)
    column_status.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
    column_status.set_fixed_width(80)
    self.todosTree.append_column(column_status)
    
    descriptiontextrenderer = gtk.CellRendererText()
    descriptiontextrenderer.set_property('wrap-mode' , pango.WRAP_CHAR)
    descriptiontextrenderer.set_property('height' , 80)
    descriptiontextrenderer.set_property('width' , -1)
    column_description = gtk.TreeViewColumn("Description", descriptiontextrenderer, markup=2)
    column_description.set_spacing(0)
    column_description.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
    self.todosTree.append_column(column_description)
    
  def edited_checkbox(self,cell, path, user_data):
    liststore, column = user_data
    liststore[path][column] = not liststore[path][column]
    #TODO SAVE data !!!
    return

  def edit(self,widget,*data):
    selection = widget.get_selection()
    model, selection_iter = selection.get_selected()
    if (selection_iter):
      uuid = model.get_value(selection_iter, 0)
      print 'uuid:',uuid
    else:
      print 'oups no selection'
  
  def __init__(self):
    hildon.Window.__init__ (self)
    p1 = hildon.PannableArea()
    self.create_treeview()
    self.todosStore.append(('1',True,'Test !'))
    self.todosStore.append(('1',True,'Test !'))
    self.todosStore.append(('1',True,'Test !'))
    self.todosStore.append(('1',True,'Test !'))
    p1.add(self.todosTree)
    self.add(p1)
    p1.show_all()
    
if __name__ == "__main__":
  t = Test()
  t.show_all()
  gtk.main()