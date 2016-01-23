"""
__init__.py

Server module file
"""

__author__ = "Sunil"
__copyright__ = "Copyleft 2015, keylogger Project"
__license__ = "GPL 3.0"
__version__ = "0.0.0"
__email__ = "sunhick@gmail.com"

import Server

import os
import logging.config

print('Setting up logging module...')

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logging.config.fileConfig('%s/logging.conf' % basepath)
logger = logging.getLogger(__name__)
