import socket

class NetSocket():

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = s


    def get_exception_type(self):
        return socket.error


    def get_fds(self):
        return self.socket,self.socket


    def connect(self):
        self.socket.connect((self.ip,self.port))


    def disconnect(self):
        self.socket.close()


    def reset(self):
        self.disconnect()
        self.connect()


    def reset(self):
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip,self.port))


    def recv(self,tlen):
        return self.socket.recv(tlen)


    def send(self,buf):
        self.socket.sendall(buf)



        