#!/usr/bin/env python

import socket
import hmac
import hashlib
import time


DEFAULT_PORT = 3456
DEFAULT_IP = "127.0.0.1"
DEFAULT_PASSWORD = "password"


class Looper():
    def __init__(self,code,port=DEFAULT_PORT,ip=DEFAULT_IP,password=DEFAULT_PASSWORD,sleep_time=0.0):
        self.port = port
        self.ip = ip
        self.password = password
        self.code = code
        if "\n" in self.code:
            raise Exception("new lines are not allowed in looper's code")
        self.sleep_time = sleep_time


    def invoke(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip,self.port))
        nounce = ""
        for i in xrange(16*2):
            nounce += s.recv(1)
        s.sendall(self.code)
        s.sendall("\n")
        s.sendall(nounce)
        mac = hmac.new(self.password,self.code+"\n"+nounce,hashlib.sha256).digest().encode('hex')
        s.sendall("\n")
        s.sendall(mac)
        s.close()
        time.sleep(self.sleep_time)


