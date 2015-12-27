import Server

import os
import logging.config

print('Setting up logging module...')

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logging.config.fileConfig('%s/logging.conf' % basepath)
logger = logging.getLogger(__name__)
