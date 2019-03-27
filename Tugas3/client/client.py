import socket
import threading
import os

SERVER_PORT = 13698
SERVER_IP = "127.0.0.1"
BLOCK_SIZE = 1024

class ClientConnection:
    def __init__(self, conn):
        print "Supported command : [ls][pwd][cd 'path'][send 'filename'][get 'filename']"
        self.conn = conn
        connInfo = conn.getsockname()
        print "Connected to " + str(connInfo[0]) + ":" + str(connInfo[1])
    def run(self):
        while True:
            request = sock.recv(BLOCK_SIZE).rstrip()
            print request,
            if request[:5] == "READY":
                cmd = raw_input()
                self.parseRequest(cmd)
            
    def parseRequest(self, request):
        if request[:2] == "cd":
            self.send("CHDIR " + request[3:])
            print self.recv().rstrip()
        elif request[:3] == "ls":
            self.send("LIST")
            print self.recv().rstrip()
        elif request[:4] == "send":
            self.sendFile(request[5:])
        elif request[:3] == "get":
            self.recvFile(request[4:])
        elif request[:3] == "pwd":
            self.send("GETCWD")
            print self.recv().rstrip()
        else:
            self.send("$")
            print self.recv().rstrip()

    def recvFile(self, fileName):
        self.send("GET " + fileName)
        ok = self.recv()
        if ok[:2] != "OK":
            print "[ERR] Invalid response : " + ok
            return
        self.send("OK")
        fp = open(fileName, "wb+")
        received = 0
        while True:
            data = self.recv()
            if data[:3] == "END":
                fp.close()
                print "End of " + fileName
                break
            else:
                fp.write(data) 
                received += len(data)
                print "Received "+ str(received)
                
    def sendFile(self, name):
        fp = None
        try:
            fp = open(name, "rb")
        except:
            print "[ERR] FILE NOT FOUND"
            return
        payload = fp.read()
        sentSize = 0
        addr = self.conn.getsockname()
        fp.close()
        self.send("PUSH "+name)
        signal = self.recv()
        if signal[:2] != "OK":
            print "[ERR] Invalid response"
            return
        for i in range((len(payload)/BLOCK_SIZE) + 1):
            data = []
            if (i+1)*BLOCK_SIZE > len(payload):
                data = payload[i*BLOCK_SIZE:len(payload)]
                sentSize += len(data)
                data.ljust(1024)
            else:
                data = payload[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE]
                sentSize += len(data)
            self.send(data)
            print "Sending "+str(sentSize) + " OF " + str(len(payload)) + " To " + str(addr[0]) + ":" + str(addr[1])
        self.send("END")

    def send(self, payload):
        self.conn.send(payload.ljust(BLOCK_SIZE))

    def recv(self):
        return self.conn.recv(BLOCK_SIZE)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP,SERVER_PORT))

conn = ClientConnection(sock)
conn.run()