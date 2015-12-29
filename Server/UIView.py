#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
UIView.py

UI view will create a server window for key logger
"""

__author__ = "Sunil"
__copyright__ = "Copyleft 2015, keylogger Project"
__license__ = "GPL 3.0"
__version__ = "0.0.0"
__email__ = "sunhick@gmail.com"


import logging
import thread
from ServerSocket import ServerSocket
from gi.repository import Gtk
from gi.repository import Pango


columns = ['Time stamp',
           'User Name',
           'Application Id',
           'Key Stroke']

keylogs = [['Dec 22, 12:50PM', 'Sunil', 'Skype', 'ALT+K'],
           ['Dec 22, 12:50PM', 'Sunil', 'Skype', 'P'],
           ['Dec 22, 12:50PM', 'Sunil', 'Skype', 'ALT+K'],
           ['Dec 22, 12:50PM', 'Sunil', 'Skype', 'P'],
           ['Dec 22, 12:50PM', 'Sunil', 'Skype', 'ALT+K'],
           ['Dec 22, 12:50PM', 'Sunil', 'Skype', 'P']]

class ServerWindow:
    """
    Server UI window for key logger
    """    
    def __init__(self):
        self._log = logging.getLogger(__name__)
        self._log.debug('Gtk window init')

        self._builder = Gtk.Builder()
        self._builder.add_from_file('gui/main_ui.glade')
        self._builder.connect_signals(self)
        self._mainwindow = self._builder.get_object('server_window')

        self._set_window_size()
        self._set_icons()
        self._setup_keylog_view()
        self._server_sock = ServerSocket()


    # ---------------------- Internal methods ------------------------

    def _setup_keylog_view(self):
        # the data in the model (three strings for each row, one for each
        # column)
        self._listmodel = Gtk.ListStore(str, str, str, str)
        # append the values in the model
        for i in range(len(keylogs)):
            self._listmodel.append(keylogs[i])

        # a treeview to see the data stored in the model
        view = Gtk.TreeView(model = self._listmodel)  # self._builder.get_object('keylog_view')
        # view.set_grid_lines(True)

        # for each column
        for i in range(len(columns)):
            # cellrenderer to render the text
            cell = Gtk.CellRendererText()
            # the text in the first column should be in boldface
            if i == 0:
                cell.props.weight_set = True
                # the column is created
            col = Gtk.TreeViewColumn(columns[i], cell, text=i)
            col.set_resizable(True)
            # and it is appended to the treeview
            view.append_column(col)

        scrolledwin = self._builder.get_object('scrolledwindow')
        scrolledwin.add(view)

    def _set_icons(self):
        self._set_resource('refresh_img', 'images/refresh.png')
        self._set_resource('delete_img', 'images/delete.png')
        self._set_resource('info_img', 'images/info.png')
        self._set_resource('hide_img', 'images/hide.png')
        self._set_resource('about_img', 'images/about.png')
        self._set_resource('stop_img', 'images/stop.png')
        self._set_resource('start_img', 'images/start.png')

    def _set_resource(self, objid, resource):
        uiobj = self._builder.get_object(objid)
        uiobj.set_from_file(resource)

    def _set_window_size(self):
        window = self.get_top_level_window()
        screen = window.get_screen()

        # collect data about each monitor
        monitors = []
        nmons = screen.get_n_monitors()
        self._log.info('There are %d monitors' % (nmons))
        
        for m in range(nmons):
            mg = screen.get_monitor_geometry(m)
            self._log.info('Monitor %d: %d x %d' % (m, mg.width, mg.height))
            monitors.append(mg)

        # current monitor
        curmon = screen.get_monitor_at_window(screen.get_active_window())
        width, height = monitors[curmon].width, monitors[curmon].height
        self._log.info('Monitor %d: %d x %d (current)' % (curmon, width, height))

        ww = 3*width/4
        wh = 3*height/4

        window.set_size_request(ww, wh)


    # ------------------- Public methods ------------------------------
    
    def get_top_level_window(self):
        return self._mainwindow

    # -------------------- Signal handlers -----------------------------
    
    def on_app_exit(self, *args):
        self._log.info('Quitting key logger app')
        Gtk.main_quit(*args)

    def start_listening(self, widget):
        self._log.debug('Clicked on Stop button')
        self._log.info('Starting listening to the key logger clients')
        # thread.start_new_thread(self._server_sock.start, (self._callback,))

    def stop_listening(self, widget):
        self._log.debug('Clicked on Start button')
        self._log.info('Stop listening to the key logger clients')
        # thread.start_new_thread(self._server_sock.stop, ())

    def aboutus(self, widget):
        self._log.debug('Clicked on About us button')
        builder = Gtk.Builder()
        builder.add_from_file('gui/about.glade')
        about_dialog = builder.get_object('about_dialog')
        about_dialog.set_transient_for(self._mainwindow)
        
        about_dialog.run()


    def information(self, widget):
        self._log.debug('Clicked on Information button')

    def hide(self, widget):
        self._log.debug('Clicked on hide button')

    def delete_log(self, widget):
        self._log.debug('Clicked on delete logs button')

    def refresh(self, widget):
        self._log.debug('Clicked on refresh button')
