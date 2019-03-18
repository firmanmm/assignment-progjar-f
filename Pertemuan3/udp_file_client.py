import socket
import os
import sys


TARGET_IP = "127.0.0.1"
TARGET_PORT = 5005
BLOCK_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fileName = "picture.png"
fileSize = os.stat(fileName).st_size

fp = open(fileName, "rb")
payload = fp.read()
sent = 0
for i in range((len(payload)/BLOCK_SIZE) + 1):
    data = []
    if (i+1)*BLOCK_SIZE > len(payload):
        data = payload[i*BLOCK_SIZE:len(payload)]
    else:
        data = payload[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE]
    sock.sendto(data, (TARGET_IP, TARGET_PORT))
    sent += sys.getsizeof(data)
    print "Sent %.0f%% with %s of data" % (float(sent)/fileSize*100.0, len(data))
fp.close()


