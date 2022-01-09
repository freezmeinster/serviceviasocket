#!/usr/bin/python
import sys
import socket
import os, os.path
import time
import json
from json.decoder import JSONDecodeError

SOCK_PATH = sys.argv[1]
KEYS = ['id', 'to', 'from', 'fizz', 'buzz']
FIZZ_DIV = 3
BUZZ_DIV = 5

if os.path.exists(SOCK_PATH):
  os.remove(SOCK_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCK_PATH)

def response(conn, msg):
    ret = bytes(msg, 'utf-8')
    conn.send(ret)

def calculate(data):
    res = []
    for a in range(int(data['from']), int(data['to']) + 1):
        if a == 0:
            res.append(data['fizz']+data['buzz'])
        elif a % FIZZ_DIV  == 0 and a % BUZZ_DIV == 0:
            res.append(data['fizz']+data['buzz'])
        elif a % FIZZ_DIV == 0:
            res.append(data['fizz'])
        elif a % BUZZ_DIV == 0:
            res.append(data['buzz'])
        else:
            res.append(a)
    return {data['id']:res}

while True:
  server.listen(1)
  conn, addr = server.accept()
  datagram = conn.recv(1024)
  if datagram:
    try:
        string = datagram.decode("utf-8")
        data = json.loads(string)
        if all([ True for x in data.keys() if x in KEYS]):
            result = calculate(data)
            response(conn,json.dumps(result))
            print("OK")
        else:
            msg = "JSON Format not match"
            response(conn,msg)
            print(msg)
        response(conn, json.dumps(data))
        conn.close()
    except JSONDecodeError:
        print("Data can't decode to JSON")
    except BrokenPipeError:
        print("Broken Pipe")

