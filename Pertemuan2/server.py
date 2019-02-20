import sys
import socket

# SOCK_STREAM = TCP, SOCK_DGRAM = UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 7777)
print 'Starting up listener on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)
while True:
    	print 'Waiting for incoming connection'
    	connection, client_address = sock.accept()
    	print 'Incoming connection from', client_address
    	while True:
        	data = connection.recv(32)
        	print 'Received data : "%s"' % data
            	if data:
                	print 'Sending data back to the client!'
                	connection.sendall('-->'+data)
            	else:
                	print 'No more data from ', client_address
                	break
	connection.close()
