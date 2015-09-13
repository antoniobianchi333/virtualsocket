#!/usr/bin/env python

import socket
import hmac
import hashlib
import time


DEFAULT_PORT = 3456
DEFAULT_IP = "127.0.0.1"
DEFAULT_PASSWORD = "password"


class Looper():
    def __init__(self,code,port=DEFAULT_PORT,ip=DEFAULT_IP,password=DEFAULT_PASSWORD):
        self.port = port
        self.ip = ip
        self.password = password
        self.code = code


    def invoke(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip,self.port))
        s.sendall(self.code)
        mac = hmac.new(self.password,self.code,hashlib.sha256).digest().encode('hex')
        s.sendall("\n"+mac)
        s.close()
        #TODO sleep is bad, but a different solution is not easy
        #a solution may be a blocking try-to-connect loop
        time.sleep(2.0)


