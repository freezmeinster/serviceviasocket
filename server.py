#!/usr/bin/python
import sys
import socket
import os, os.path
import time
import json
from json.decoder import JSONDecodeError

if len(sys.argv) > 1:
    SOCK_PATH = sys.argv[1]
else:
    SOCK_PATH = "/root/share/socks.sock"

KEYS = ['id', 'to', 'from', 'fizz', 'buzz']
FIZZ_DIV = 3
BUZZ_DIV = 5

if os.path.exists(SOCK_PATH):
    os.remove(SOCK_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCK_PATH)
os.chmod(SOCK_PATH, 0o777)

def response(conn, msg):
    ret = bytes(msg, 'utf-8')
    conn.send(ret)

def calculate(data):
    res = []
    for a in range(int(data['from']), int(data['to']) + 1):
        if a % FIZZ_DIV  == 0 and a % BUZZ_DIV == 0:
            res.append(data['fizz']+data['buzz'])
        elif a % FIZZ_DIV == 0:
            res.append(data['fizz'])
        elif a % BUZZ_DIV == 0:
            res.append(data['buzz'])
        else:
            res.append(a)
    return {data['id']:res}

while True:
    try:
        server.listen(1)
        conn, addr = server.accept()
        datagram = conn.recv(1024)
        if datagram:
            try:
                final = list()
                string = datagram.decode("utf-8")
                for item in string.split():
                    data = json.loads(item)
                    if all([ (True if x in data.keys() else False ) for x in KEYS]):
                        final.append(calculate(data))
                        print("OK")
                    else:
                        msg = "JSON Format not match =>> %s" % item
                        final.append(msg)
                        print(msg)
                final_string = "\n".join([json.dumps(x) for x in final])
                response(conn, final_string + "\n")
                conn.close()
            except JSONDecodeError:
                print("Data can't decode to JSON")
            except BrokenPipeError:
                print("Broken Pipe")
    except KeyboardInterrupt:
        print('Force shutdown, try to cleanup socket')
        os.unlink(SOCK_PATH)
        print("Good bye")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
