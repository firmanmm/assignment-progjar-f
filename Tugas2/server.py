from threading import Thread
import socket

BIND_IP = "127.0.0.1"
BIND_PORT = 9000
BLOCK_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((BIND_IP, BIND_PORT))

def waitRequest():
    while True:
        print "Waiting"
        data, addr = sock.recvfrom(1024)
        print "Receiving : " + str(data)
        if str(data) == "REQ":
            thread = Thread(target=processRequest, args=(addr))
            thread.start()
        
def processRequest(ip, port):
    addr = (ip, port)
    sendFile("gerhana.jpg", addr)
    sendFile("GGJ2017.jpg", addr)
    sendFile("index.jpg", addr)
    sendFile("kitten.jpg", addr)
    sendFile("picture.png", addr)
    sock.sendto("CLOSE".ljust(1024), addr)

def sendFile(name, addr):
    fp = open(name, "rb")
    payload = fp.read()
    sentSize = 0
    fp.close()
    sock.sendto(("START " + name).ljust(1024), addr)
    for i in range((len(payload)/BLOCK_SIZE) + 1):
        data = []
        if (i+1)*BLOCK_SIZE > len(payload):
            data = payload[i*BLOCK_SIZE:len(payload)]
            sentSize += len(data)
            data.ljust(1024)
        else:
            data = payload[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE]
            sentSize += len(data)
        sock.sendto(data, addr)
        print "Sending "+str(sentSize) + " OF " + str(len(payload)) + " To " + str(addr[0]) + ":" + str(addr[1])
    sock.sendto(("END " + name).ljust(1024), addr)

while True:
    waitRequest()