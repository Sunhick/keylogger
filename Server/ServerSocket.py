import sys
import logging
import thread
from socket import *


BUFFER = 10  # read 10 chars at a time

class ServerSocket(object):
    def __init__(self):
        self._log = logging.getLogger(__name__)
        # Create a TCP/IP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._threads = []
        self._server_up = True

    def start(self):
        # Bind the socket to the port
        server_address = ('localhost', 9999)
        self._log.info('starting up on %s port %s' % (server_address))
        self._sock.bind(server_address)
        # Listen for incoming connections
        self._sock.listen(1)

        while _server_up:
            # Wait for a connection
            self._log.debug('waiting for a connection')
            connection, client_address = sock.accept()
            try:
                self._log.info('connection from {0}' % (client_address))
                clienthandler = thread.start_new_thread(self.handler, (connection, client_address))
                self._threads.append(client_address)
            except Exception, exp:
                self._log.error(e, exc_info = True)


    def stop(self):
        self._log.info('stop server socket listen')
        self._server_up = False

    def handler(self, clientsock, addr):
        while True:
            data = clientsock.recv(BUFFER)
            self._log.info('Data:' + repr(data))
            
            if not data:
                break

        clientsock.close()
