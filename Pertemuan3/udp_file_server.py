import socket

BIND_IP = "127.0.0.1"
BIND_PORT = 5005
fileName = "output.out"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((BIND_IP, BIND_PORT))

fp = open(fileName, "wb+")

while True:
    data, addr = sock.recvfrom(1024)
    print "%s : %s" % (addr, data)
    fp.write(fileName)

fp.close()