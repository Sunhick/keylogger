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


class ServerWindow(Gtk.Window):
    """
    Server UI window for key logger
    """    
    def __init__(self):
        self._log = logging.getLogger(__name__)
        self._log.debug('Gtk window init')
        Gtk.Window.__init__(self, title = 'Key logger')

        self._grid = Gtk.Grid()
        self.add(self._grid)

        self._start_button = Gtk.Button(label="Start")
        self._start_button.connect("clicked", self.start_listening)
        self._grid.add(self._start_button)

        self._stop_button = Gtk.Button(label="Stop")
        self._stop_button.connect("clicked", self.stop_listening)
        self._grid.add(self._stop_button)

        self._server_sock = ServerSocket()

    def start_listening(self, widget):
        self._log.info('Starting listening to the key logger clients')
        thread.start_new_thread(self._server_sock.start, ())

    def stop_listening(self, widget):
        self._log.info('Stop listening to the key logger clients')
        thread.start_new_thread(self._server_sock.stop, ())
