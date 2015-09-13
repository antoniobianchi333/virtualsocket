
import socket
import time
import re
import select
import sys
from socket import error


class CommunicationException(Exception):
    def __init__(self,msg,data):
        super(CommunicationException, self).__init__(msg)
        self.data = data


class VirtualSocket(object):
    def __init__(self,gsocket,auto_flush=True,looper=None):
        self.gsocket = gsocket
        self.flow = []
        self.auto_flush = auto_flush
        self.tsent = ""
        self.send_buffer = ""
        self.looper = looper

    def connect(self):
        if self.looper != None:
            self.looper.invoke()
        self.gsocket.connect()

    def log_send(self,data):
        self.tsent += data

    def log_flush(self):
        self.flow.append(("send",self.tsent))
        self.tsent = ""

    def log_recv(self,data):
        self.flow.append(("recv",data))

    def handle_exception(self,msg,data):
        self.log_recv(data)
        raise CommunicationException(msg,data)

    #inspired by telnet.interact()
    def interact(self):
        print '*** Starting interactive session ***'
        try:
            while True:
                recv_socket = self.gsocket.get_fds()[0]
                rfd, wfd, xfd = select.select([recv_socket, sys.stdin], [], [])
                if recv_socket in rfd:
                    try:
                        text = self.gsocket.recv(1)
                    except self.gsocket.get_exception_type():
                        print '*** Connection closed by remote host ***'
                        break
                    if text:
                        sys.stdout.write(text)
                        sys.stdout.flush()
                    else:
                        print '*** Connection closed by remote host (empty data recv) ***'
                        break
                elif sys.stdin in rfd:
                    line = sys.stdin.readline()
                    if not line:
                        break
                    try:
                        self.gsocket.send(line)
                    except self.gsocket.get_exception_type():
                        print '*** Exception during send ***'
                        break

        except KeyboardInterrupt:
            print "*** interact interrupted ***"


    def reset(self):
        self.gsocket.reset()


    def recv(self,tlen):
        if type(tlen) == str:
            tlen = len(tlen)

        data = ""
        while len(data) < tlen:
            try:
                recv_socket,_ = selectlf.gsocket.get_fds()
                rfd, wfd, xfd = select.select([recv_socket], [], [recv_socket])
                if recv_socket in rfd:
                    tdata = self.gsocket.recv(1)
                elif recv_socket in xfd:
                    msg = "Problem during select 1: (%5s):%s" % (len(data),repr(data))
                    self.handle_exception(msg,data)
                else:
                    msg = "Problem during select 2: (%5s):%s" % (len(data),repr(data))
                    self.handle_exception(msg,data)
            except self.gsocket.get_exception_type():
                etype, value, traceback = sys.exc_info()
                msg = "Exception during recv (%s,%s): (%5s):%s" % (etype,value,len(data),repr(data))
                self.handle_exception(msg,data)
            except KeyboardInterrupt:
                msg = "Recv interrupted: (%5s):%s" % (len(data),repr(data))
                self.handle_exception(msg,data)
            if len(tdata) == 0:
                msg = "Socket disconnected while recv: (%5s):%s" % (len(data),repr(data))
                self.handle_exception(msg,data)
            else:
                data += tdata

        self.log_recv(data)
        return data


    def recv_until(self,delim):
        data = ""
        while True:
            try:
                recv_socket,_ = self.gsocket.get_fds()
                rfd, wfd, xfd = select.select([recv_socket], [], [recv_socket])
                if recv_socket in rfd:
                    tdata = self.gsocket.recv(1)
                elif recv_socket in xfd:
                    msg = "Problem during select 1: (%5s):%s" % (len(data),repr(data))
                    self.handle_exception(msg,data)
                else:
                    msg = "Problem during select 2: (%5s):%s" % (len(data),repr(data))
                    self.handle_exception(msg,data)
            except self.gsocket.get_exception_type():
                etype, value, traceback = sys.exc_info()
                msg = "Exception during recv (%s,%s): (%5s):%s" % (etype,value,len(data),repr(data))
                self.handle_exception(msg,data)
            except KeyboardInterrupt:
                msg = "Recv interrupted: (%5s):%s" % (len(data),repr(data))
                self.handle_exception(msg,data)
            if len(tdata) == 0:
                msg = "Socket disconnected while recv: (%5s):%s" % (len(data),repr(data))
                self.handle_exception(msg,data)
            else:
                data += tdata
            if(data.endswith(delim)):
                break

        self.log_recv(data) 
        return data

    def recv_until_regex(self,regex):
        if type(regex) == str:
            com = re.compile(regex,re.DOTALL)
        else:
            com = regex

        data = ""
        while True:
            try:
                recv_socket,_ = self.gsocket.get_fds()
                rfd, wfd, xfd = select.select([recv_socket], [], [recv_socket])
                if recv_socket in rfd:
                    tdata = self.gsocket.recv(1)
                elif recv_socket in xfd:
                    msg = "Problem during select 1: (%5s):%s" % (len(data),repr(data))
                    self.handle_exception(msg,data)
                else:
                    msg = "Problem during select 2: (%5s):%s" % (len(data),repr(data))
                    self.handle_exception(msg,data)
            except self.gsocket.get_exception_type():
                etype, value, traceback = sys.exc_info()
                msg = "Exception during recv (%s,%s): (%5s):%s" % (etype,value,len(data),repr(data))
                self.handle_exception(msg,data)
            except KeyboardInterrupt:
                msg = "Recv interrupted: (%5s):%s" % (len(data),repr(data))
                self.handle_exception(msg,data)
            if len(tdata) == 0:
                msg = "Socket disconnected while recv: (%5s):%s" % (len(data),repr(data))
                self.handle_exception(msg,data)
            else:
                data += tdata

            if(com.match(data)):
                break

        self.log_recv(data) 
        return data

    #this is bad: do not use it! :-)
    #wait until we do not recv any new data for 0.2 seconds
    #blocking until "something" is received
    def recv_all(self):
        data = ""
        while True:
            try:
                timeout = False
                recv_socket,_ = self.gsocket.get_fds()
                rfd, wfd, xfd = select.select([recv_socket], [], [recv_socket],0.2)
                if recv_socket in rfd:
                    tdata = self.gsocket.recv(1024*1024)
                elif recv_socket in xfd:
                    msg = "Problem during select 1: (%5s):%s" % (len(data),repr(data))
                    self.handle_exception(msg,data)
                else: #timeout
                    if data != "":
                        break
                    else:
                        tdata = ""
                        timeout = True
            except self.gsocket.get_exception_type():
                etype, value, traceback = sys.exc_info()
                msg = "Exception during recv (%s,%s): (%5s):%s" % (etype,value,len(data),repr(data))
                self.handle_exception(msg,data)
            except KeyboardInterrupt:
                msg = "Recv interrupted: (%5s):%s" % (len(data),repr(data))
                self.handle_exception(msg,data)
            if len(tdata) == 0 and not timeout:
                msg = "Socket disconnected while recv: (%5s):%s" % (len(data),repr(data))
                self.handle_exception(msg,data)
            else:
                data += tdata

        self.log_recv(data)
        return data


    def recv_time(self,timeout=5.0):
        data = ""
        start_time = time.time()
        try:
            while True:
                tdata = ""
                time.sleep(0.01) #avoid unlimited looping when connection is closed
                current_time = time.time()
                elapsed_time = current_time - start_time
                if elapsed_time>timeout:
                    break
                try:
                    recv_socket,_ = self.gsocket.get_fds()
                    rfd, wfd, xfd = select.select([recv_socket], [], [recv_socket],timeout-elapsed_time)
                    #print rfd, wfd, xfd,timeout-elapsed_time
                    if recv_socket in rfd:
                        tdata = self.gsocket.recv(1024*1024)
                except self.gsocket.get_exception_type():
                    pass

                data += tdata

        except KeyboardInterrupt:
            msg = "Recv interrupted: (%5s):%s" % (len(data),repr(data))
            self.handle_exception(msg,data)

        self.log_recv(data)
        return data


    def disconnect(self):
        self.gsocket.disconnect()


    def reset(self):
        self.gsocket.reset()


    def send(self,buf):
        self.log_send(buf)
        self.send_buffer += buf
        if self.auto_flush :
            self.flush()


    def flush(self,sleep_time=0.0):
        self.log_flush()
        try:
            self.gsocket.send(self.send_buffer)
        except:
            etype, value, traceback = sys.exc_info()
            raise CommunicationException("Exception while sending data",repr(self.send_buffer))
        self.send_buffer = ""
        time.sleep(sleep_time)





