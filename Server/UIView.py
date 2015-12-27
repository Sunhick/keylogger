#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
UIView.py

UI view will create a server window for key logger
"""

__author__ = "Sunil"
__copyright__ = "Copyleft 2015, keylogger Project"
__license__ = "GPL 3.0"
__version__ = "1.0.0"
__email__ = "sunhick@gmail.com"


import logging
from gi.repository import Gtk


class ServerWindow(Gtk.Window):
    """
    Server UI window for key logger
    """    
    def __init__(self):
        self._log = logging.getLogger(__name__)
        self._log.debug('Gtk window init')
        Gtk.Window.__init__(self, title = 'Key logger')

        self.button = Gtk.Button(label = 'Quit')
        self.button.connect('clicked', self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        self._log.info('button clicked')
