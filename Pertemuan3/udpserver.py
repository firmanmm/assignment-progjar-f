import socket

BIND_IP = "127.0.0.1"
BIND_PORT = 5005


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((BIND_IP, BIND_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print "%s : %s" % (addr, data)