import sys
import traceback
import hildon
import gtk
import osso

APP_NAME = "Default App Name"
APP_VERSION = "Default Version"

#Here is the installation of the hook. Each time a untrapped/unmanaged exception will
#happen my_excepthook will be called.
def install_excepthook(app_name,app_version):
    global APP_NAME
    global APP_VERSiON

    APP_NAME = app_name
    APP_VERSION = app_version
  
    def my_excepthook(exctype, value, tb):
        #traceback give us all the errors information message like the method, file line ... everything like
        #we have in the python interpreter 
        s = ''.join(traceback.format_exception(exctype, value, tb))
        formatted_text = "%s Version %s\nTrace : %s\nComments : " (str(APP_NAME), str(APP_VERSION), s)
        #here is just my own gtk dialog you can replace it by what you want
        ErrorReportDialog(formatted_text)

    sys.excepthook = my_excepthook

#Display errors in an hildon way
def error():
    note = osso.SystemNote(osso.Context('net.khertan.bugreporter','1.0.0', False))
    result = note.system_note_infoprint("Error occurs during the report")

#The trick to report bugs directly in Flyspray with my bugreport php extension for flyspray
def Report(text,email):
    import urllib
    import urllib2

    url = 'http://khertan.net/flyspray/bugreport.php?do=newtask&project=2' # write ur URL here
    values = {
          'project_id' : '2',
          'item_summary': text.split('\n')[0],
          'task_type':'1',
          'product_category':'0',
          'task_severity':'2',
          'task_priority':'2',
          'product_version':'1',
          'detailed_desc':text+'\nReported by '+email,
          'anon_email':email,
          }

    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        if the_page == '200':
          return True
        else:
        print response
          error()
          return False
  except Exception, detail:
      error()
      print detail
      return False

#A small gtk Dialog
def ErrorReportDialog(trace,txt_email=None):
  dialog = gtk.Dialog('Report Bug',hildon.Window(),gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_OK,gtk.RESPONSE_ACCEPT))
  p = hildon.PannableArea()
  email = hildon.Entry(0)
  if txt_email == None:
    email.set_placeholder_text('Email')
  else:
    email.set_text(txt_email)
  report = hildon.TextView()
  report.set_wrap_mode(gtk.WRAP_CHAR)
  report.get_buffer().set_text(trace)
  vbox = gtk.VBox()
  vbox.set_homogeneous(False)
  p.add_with_viewport(vbox)
  vbox.pack_start(email,expand=False,fill=False)
  report.set_size_request(-1,-1)
  vbox.add(report)
  p.show_all()
  dialog.set_focus(report)
  dialog.vbox.set_size_request(-1,300)
  dialog.vbox.add(p)
  if(dialog.run()==gtk.RESPONSE_ACCEPT):
    start,end = report.get_buffer().get_bounds()
    if Report(report.get_buffer().get_text(start,end),email.get_text()):
      dialog.destroy()
    else:
      text = report.get_buffer().get_text(start,end)
      txt_email = email.get_text()
      dialog.destroy()
      ErrorReportDialog(text,txt_email)
  else:
    dialog.destroy()

#Small test of a use from a about menu for example
if __name__ == "__main__":
  ErrorReportDialog('PyGTKEditor Version 3.0.15\nEvolution implement bug report\nComments: Any')
