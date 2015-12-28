import sys
import logging
import thread
import socket


BUFFER = 50  # read 10 chars at a time
BACKLOG = 5  # allow upto 5 clients at a time to connect to server

class ServerSocket(object):
    def __init__(self):
        self._log = logging.getLogger(__name__)
        self._threads = []

    def start(self, callback):
        self._server_up = True
        
        # Create a TCP/IP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the port
        server_address = ('localhost', 9999)
        self._log.info('starting up on %s port %s' % (server_address))
        self._sock.bind(server_address)
        
        # Listen for incoming connections
        self._sock.listen(BACKLOG)

        while self._server_up:
            # Wait for a connection
            self._log.debug('waiting for a connection')
            connection, client_address = self._sock.accept()
            self._log.debug('connection from {addr}'.format(addr=client_address))
            try:
                clienthandler = thread.start_new_thread(self.handle_client,
                                                        (connection, client_address, callback))
                self._threads.append(client_address)
            except Exception, exp:
                self._log.error('Exception occured during starting thread')
                self._log.exception(exp)

        self._log.debug('No more listening for client requests')

    def stop(self):
        self._log.info('stop server socket listen')
        self._server_up = False
        self._sock.close()

    def handle_client(self, clientsock, addr, callback):
        self._log.info('reading data from client {addr}'.format(addr=addr))
        while self._server_up:
            data = clientsock.recv(BUFFER)
            self._log.info('Data:' + repr(data))
            callback(repr(data))
            
            if not data:
                break

        clientsock.close()
