# virtualsocket
a nice library to interact with binaries (mainly developed for CTF exploits)

## installation


```bash
git clone https://github.com/antoniobianchi333/virtualsocket.git
pip install -e virtualsocket/
```

## usage
virtualsocket can be used transparently with binaries using either a TCP socket or stdout/stdin

### using with TCP binaries
#### importing
```python
from virtualsocket.virtualsocket import VirtualSocket
from virtualsocket.gsocket.netsocket import NetSocket
```
#### connecting
```python
#suppose that your binary is listening on 127.0.0.1:7777
vs = VirtualSocket(NetSocket("127.0.0.1",7777))
vs.connect()
```

### using with stdin/stderr binaries
#### importing
```python
from virtualsocket.virtualsocket import VirtualSocket
from virtualsocket.gsocket.stdsocket import StdSocket
```
#### opening the binary
```bash
mkfifo /tmp/in
mkfifo /tmp/out
./my_std_binary < /tmp/out > /tmp/in
```
If you need to use GDB:
```bash
gdb ./my_std_binary
r < /tmp/out > /tmp/in
```
If programmed correctly, std binaries should flush the pipes correctly (by either calling _flush_ or setting the buffering properly using _setvbuf_).

In case of problems, you can try:
```bash
unbuffer ./my_std_binary < /tmp/out > /tmp/in
```
or
```bash
stdbuf -i 0 -o 0 -e 0 ./my_std_binary < /tmp/out > /tmp/in
```

#### connecting
```python
#suppose that your binary has been opened with: ./my_std_binary < /tmp/out > /tmp/in
vs = VirtualSocket(StdSocket("/tmp/in","/tmp/out"))
vs.connect()
```

### communicating
#### Send and receive data
```python
#send data
vs.send("datadatadata\n")

#receive 10 bytes
data = vs.recv(10)

#receive until the string "endofmessage"
data = vs.recv_until("endofmessage")

#receive until the word FLAG followed by three digits
data = vs.recv_until_regex(".*FLAG\d\d\d")

#receive everything for 2 seconds
data = vs.recv_time(2.0)

#receive "all":
#wait until we do not recv any new data for 0.2 seconds, blocking until "something" is received
data = vs.recv_all() #you should never use recv_all if you want reliable code!
```

#### Exceptions
```python
#In case of communication problems (e.g., socket disconnected) or interrupted recv/send a CommunicationException is generated
from virtualsocket.virtualsocket import CommunicationException
try:
    vs.recv_time(10.0)
except CommunicationException, e:
    #we get here if the connection dies within 10 seconds
    #you can access data received before the exception
    data_received_so_far = e.data
```

#### Advanced features
```python
#open interactive shell
vs.interact()

#get the entire communication history
vs.flow()

#CTRL+C
'''
At any time, while blocked in a recv, you can press CTRL+C.
Data received between the last recv and CTRL+C will be printed.
'''


