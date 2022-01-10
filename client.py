import socket
import sys

SOCK_PATH = sys.argv[1]

def sendsock(payload):
    s = socket.socket(
        socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(SOCK_PATH)
    s.send(payload.encode("utf-8"))
    datagram = s.recv(1024)
    if datagram:
        string = datagram.decode("utf-8")
        print(repr(string))
    s.close()

sendsock("""{"id":"one","from":0,"to":5,"fizz":"zzif","buzz":"zzub"}\n""")
sendsock("""{"id":"one","from":0,"to":5,"fizz":"zzif","buzz":"zzub"}\n{"id":"two","from":6,"to":10,"fizz":"zzif2","buzz":"zzub2"}\n""")
sendsock("""{"id":"one","from":0,"to":5,"fizz":"zzif"}\n{"id":"two","from":6,"to":10,"fizz":"zzif2","buzz":"zzub2"}\n""")
