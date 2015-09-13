#!/usr/bin/env python

import socket
import os
import signal
import subprocess
import select
import argparse
import hmac
import hashlib

DEFAULT_PORT = 3456
DEFAULT_IP = "127.0.0.1"
DEFAULT_PASSWORD = "password"


#from: https://gist.github.com/thepaul/1206753
def become_tty_fg(child=True):
    os.setpgrp()
    hdlr = signal.signal(signal.SIGTTOU, signal.SIG_IGN)
    tty = os.open('/dev/tty', os.O_RDWR)
    os.tcsetpgrp(tty, os.getpgrp())
    if child:
        signal.signal(signal.SIGTTOU, hdlr)


def wait_socket_and_process(s,process):
    while True:
        rr,_,_ = select.select([s],[],[],0.1)
        if len(rr)>0:
            conn, addr = rr[0].accept()
            if process != None:
                os.killpg(process.pid,9)
                process.poll()
                become_tty_fg(False)
                subprocess.Popen("reset",shell=True).communicate()
                print "* subprocess killed"
            return conn,addr
        elif (process != None and process.poll() != None):
            become_tty_fg(False)
            process = None
            print "* subprocess terminated"

#TODO with this implementation, replay attacks are still possible
def parse_and_verify_cmd(tstr,password):
    def constant_time_compare(val1, val2):
        #from django source code
        if len(val1) != len(val2):
            return False
        result = 0
        for x, y in zip(val1, val2):
            result |= ord(x) ^ ord(y)
        return result == 0


    cmd,_,remote_mac = tstr.partition("\n")
    local_mac = hmac.new(password,cmd,hashlib.sha256).digest().encode('hex')
    if constant_time_compare(remote_mac,local_mac):
        return cmd
    else:
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Looper process to be used in conjunction with virtulsocket library.')
    parser.add_argument('--ip',type=str,help='ip on which the looper will listen',default=DEFAULT_IP)
    parser.add_argument('--port',type=int,help='port on which the looper will listen',default=DEFAULT_PORT)
    parser.add_argument('--password',type=str,help='password',default=DEFAULT_PASSWORD)
    args = parser.parse_args()

    if args.password == DEFAULT_PASSWORD:
        print "WARNING:", "using default password allows arbitrary code execution to anyone that can connect to ",args.ip+":"+str(args.port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((args.ip, args.port))
    s.listen(1)

    process = None
    try:
        while True:
            print "*** waiting from new connections on:",args.ip,str(args.port)
            conn,addr = wait_socket_and_process(s,process)
            print "*** new connection from",addr

            full_data = ""
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                full_data += data

            cmd = parse_and_verify_cmd(full_data,args.password)
            if cmd == None:
                print "* invalid command received"
                continue
            else:
                print "* executing command",cmd
            process = subprocess.Popen(cmd,preexec_fn=become_tty_fg,shell=True)

    except KeyboardInterrupt:
        print "*** terminating..."
        if (process != None and process.poll() == None):
            os.killpg(process.pid,9)
            process.poll()
            subprocess.Popen("reset",shell=True).communicate()
        become_tty_fg(False)
    

