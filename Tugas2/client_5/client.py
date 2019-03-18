import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 9000
BLOCK_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fp = None
fileName = None
received = 0
print "Sending Request"
sock.sendto("REQ", (TARGET_IP, TARGET_PORT))
while True:
    data, addr = sock.recvfrom(BLOCK_SIZE)
    if data[:5] == "START":
        fileName = data[6:].replace(" ", "")
        received = 0
        fp = open(fileName, "wb+")
        print "Start of " + fileName
    elif data[:3] == "END":
        fp.close()
        print "End of " + fileName
    elif data[:5] == "CLOSE":
        print "Closing connection"
        break
    else:
        fp.write(data)
        received += len(data)
        print "Received "+ str(received)
print "Finished Operation"