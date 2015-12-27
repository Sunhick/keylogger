#!/usr/bin/python

"""
Server.py

Server implementation of the keylogger. All the clients 
"""

__author__ = "Sunil"
__copyright__ = "Copyleft 2015, keylogger Project"
__license__ = "GPL 3.0"
__version__ = "1.0.0"
__email__ = "sunhick@gmail.com"


import sys
import Tkinter


def main(*argv):
    srv_window = Tkinter.Tk()
    srv_window.mainloop()


if __name__ == '__main__':
    main(sys.argv)
