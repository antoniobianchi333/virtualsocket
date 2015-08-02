#!/usr/bin/env python

import os

class StdSocket():

    #auto spawn mode with params and internal pipe
    def __init__(self,fin_name,fout_name,create_file=False):
        if create_file:
            try:
                os.mkfifo(fin_name)
                os.mkfifo(fout_name)
            except OSError:
                pass
        self.fin_name = fin_name
        self.fout_name = fout_name


    def get_exception_type(self):
        return OSError

    def get_fds(self):
        return self.fin,self.fout

    def connect(self):
        self.fin = os.open(self.fin_name,os.O_RDONLY|os.O_NONBLOCK)
        self.fout = os.open(self.fout_name,os.O_WRONLY|os.O_NONBLOCK)

    def disconnect(self):
        os.close(self.fin)
        ps.close(self.fout)

    def reset(self):
        self.disconnect()
        self.connect()

    def recv(self,tlen):
        return os.read(self.fin,tlen)

    def send(self,buf):
        os.write(self.fout,buf)




