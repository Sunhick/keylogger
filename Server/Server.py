#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Server.py

Server implementation of the keylogger. All the clients 
will hook to the server socket and send the key strokes.
"""

__author__ = "Sunil"
__copyright__ = "Copyleft 2015, keylogger Project"
__license__ = "GPL 3.0"
__version__ = "0.0.0"
__email__ = "sunhick@gmail.com"


import sys
import logging
import os
import logging.config

from UIView import ServerWindow
from gi.repository import Gtk


# set up the logging
print('Setting up logging module...')
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
print basepath
logging.config.fileConfig('%s/logging.conf' % basepath)
log = logging.getLogger(__name__)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    log.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def main(*argv):
    # catch global unhandled exceptions
    sys.excepthook = handle_exception
    
    log.debug('Creating Gtk window')
    win = ServerWindow()

    log.debug('Hooking delete-event to Gtk quit')
    win.connect('delete-event', Gtk.main_quit)

    log.debug('starting root window in maximized state')
    win.maximize()
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main(sys.argv)
