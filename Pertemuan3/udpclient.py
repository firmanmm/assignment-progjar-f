import socket
import time

TARGET_IP = "127.0.0.1"
TARGET_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
i = 0
while True:
    i += 1
    msg = "Number {}" . format(i)
    print msg
    sock.sendto(msg, (TARGET_IP, TARGET_PORT))
    time.sleep(1)