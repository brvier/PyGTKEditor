#!/usr/bin/python
# -*- coding: utf-8 -*-

import hildon
import gtk
import commands
import pge_report

class Dialog(hildon.Dialog):
  def __init__(self,app_name,app_version,app_description,app_icon,app_licence,donation_link,report_link):
    hildon.Dialog.__init__ (self)
    self.set_title('About '+app_name)
    self.set_size_request(-1,300)
    self.vbox.add(gtk.image_new_from_icon_name('pygtkeditor',gtk.ICON_SIZE_DIALOG))
    l = gtk.Label()
    l.set_markup('<span size="x-large">'+app_name+' '+app_version+'</span>')
    self.vbox.add(l)
    l = gtk.Label()
    l.set_markup('<span size="small" foreground="lightgrey">'+app_description+'</span>')
    self.vbox.add(l)
    l = gtk.Label()
    l.set_markup('<span size="small" foreground="lightgrey">By Benoît HERVIER (Khertan)</span>')
    self.vbox.add(l)
    l = gtk.Label()
    l.set_markup('<span size="small" foreground="lightgrey">Licence : '+app_licence+'</span>')
    self.vbox.add(l)
    hbox = gtk.HBox()
    link_b = hildon.Button(0,0)
    link_b.set_title('Visit Khertan.net')
    link_b.connect('clicked',self.open_link,report_link)
    hbox.add(link_b)
    bugs_b = hildon.Button(0,0)
    bugs_b.set_title('Report Bug')
    bugs_b.connect('clicked',self.open_report_ui,app_name,app_version)
    hbox.add(bugs_b)
#    donate_b = hildon.Button(0,0)
#    donate_b.set_title('Make a Donation')
#    donate_b.connect('clicked',self.open_link,donation_link)
#    hbox.add(donate_b)
    self.vbox.add(hbox) 
    self.vbox.show_all()

  def open_report_ui(self,widget,app_name,app_version):
    pge_report.ErrorReportDialog(app_name+' Version '+app_version+'\nEXACT STEPS LEADING TO PROBLEM: \n\nEXPECTED OUTCOME:\n\nACTUAL OUTCOME: \n')

  def open_link(self,widget,link):
    commands.getoutput('browser_dbuscmd.sh load_url '+link)
    self.hide()

if __name__ == "__main__":
  d = Dialog('PyGTKEditor','3.0.11','blabla blablabla blabla blabla blablabla blabla blabla blablabla blabla','pygtkeditor','GPLv2','http://khertan.net/','http://bugs.maemo.org')
  d.run()
  print 'something'
  d.destroy()
  gtk.main()
