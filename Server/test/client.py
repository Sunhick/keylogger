import socket
import sys
import argparse

def get_adapter_ip(adapter):
    import os
    if os.name != 'nt':
        import fcntl
        import struct

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(
            fcntl.ioctl(sock.fileno(), 0x8915,
                        struct.pack('256s', adapter[:15]))[20:24])


HOST, PORT = get_adapter_ip('wlp4s0'), 9999
data = 'Dec 22 1:34PM ||Sunil||Emacs||Emacs-lucid||ALT+M'

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data)

    # Receive data from the server and shut down
    # received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     {}".format(data)
