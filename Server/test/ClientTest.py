import socket
import sys

HOST, PORT = "localhost", 9999
data = 'Dec 22 1:34PM |Sunil|Emacs|ALT+M'

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
