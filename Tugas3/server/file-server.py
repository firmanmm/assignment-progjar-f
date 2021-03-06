import socket
import threading
import os

BIND_PORT = 13698
BIND_IP = "127.0.0.1"
BLOCK_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((BIND_IP, BIND_PORT))
sock.listen(5)

class ActiveConnection:
    def __init__(self,conn):
        self.conn = conn
        self.cwd = os.path.dirname(os.path.realpath(__file__))

    def handleRequest(self):
        while True:
            self.send("READY $"+self.cwd+": ")
            data = self.conn.recv(BLOCK_SIZE)
            sockInfo = self.conn.getsockname()
            if len(data) == 0:
                print "Closing connection with " + str(sockInfo[0]) + ":" + str(sockInfo[1])
                return
            else:
                self.parseRequest(data)
                

    def parseRequest(self, request):
        if request[:4] == "LIST":
            self.sendList()
        elif request[:6] == "GETCWD":
            self.sendPwd()
        elif request[:5] == "CHDIR":
            self.changeDir(request[6:].rstrip())
        elif request[:3] == "GET":
            self.sendFile(request[4:].rstrip())
        elif request[:4] == "PUSH":
            self.recvFile(request[5:].rstrip())
        else:
            self.send("[ERR] No matching request")

    def recvFile(self, fileName):
        fp = open(fileName, "wb+")
        self.send("OK")
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
            fp = open(self.cwd + "/" + name, "rb")
            self.send("OK")
        except e:
            self.send("[ERR] " + e)
            return
        payload = fp.read()
        sentSize = 0
        addr = self.conn.getsockname()
        fp.close()
        while True:
            signal = self.recv()
            if signal[:2] == "OK":
                break
            else:
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

    def changeDir(self, target):
        try:
            oldDir = os.getcwd()
            os.chdir(self.cwd + "/" + target)
            self.cwd = os.getcwd()
            os.chdir(oldDir)
            self.send("Moved to " + "/" + self.cwd)
        except:
            self.send("[ERR] Dir not found")

    def sendList(self):
        files = os.listdir(self.cwd)
        res = ""
        for file in files:
            res += file + "\n"
        self.send(res)

    def sendPwd(self):
        self.send(self.cwd)

    def send(self, packet):
        self.conn.send(packet.ljust(BLOCK_SIZE))

    def recv(self):
        return self.conn.recv(BLOCK_SIZE)

while True:
    print "Waiting"
    conn, addr = sock.accept()
    print 'Incoming connection from', addr
    activeConn = ActiveConnection(conn)
    thread = threading.Thread(target=activeConn.handleRequest)
    thread.start()

            

			