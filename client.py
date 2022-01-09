import socket
import sys

SOCK_PATH = sys.argv[1]

s = socket.socket(
    socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(SOCK_PATH)
s.send(b'{"id":"one","from":0,"to":15,"fizz":"zzif","buzz":"zzub"}\n')
datagram = s.recv(1024)
if datagram:
    string = datagram.decode("utf-8")
    print(string)
s.close()
