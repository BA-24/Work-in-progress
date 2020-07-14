import socket
import select
import errno
import sys
 
headerLength = 10
ip = "192.168.1.240"
port = 2
 
username = input("Username: ")
channel = input("Channel: ")
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientSocket.connect((ip, port))
except ConnectionRefusedError:
    print('No connection found')
    sys.exit()
clientSocket.setblocking(False)
 
username = username.encode("utf-8")
usernameHeader = f"{len(username):<{headerLength}}".encode("utf-8")
channel = channel.encode("utf-8")
channelHeader = f"{len(channel):<{headerLength}}".encode("utf-8")
send = usernameHeader + username + channelHeader + channel
sendHeader = f"{len(send):<{headerLength}}".encode("utf-8")
 
clientSocket.send(sendHeader + send)
 
testList = [usernameHeader, username, channelHeader, channel]
for x in testList:
    print(x.decode("utf-8"))
 
def rMsg(): #receive message
    try:
        headerLength = 10
        usernameHeader = clientSocket.recv(headerLength)
        if not len(usernameHeader):
            return False, "Server closed"
        usernameLength = int(usernameHeader.decode("utf-8").strip())
        username = clientSocket.recv(usernameLength).decode("utf-8")
        messageHeader = clientSocket.recv(headerLength)
        messageLength = int(messageHeader.decode("utf-8").strip())
        message = clientSocket.recv(messageLength).decode("utf-8")
 
        return username, message
    except IOError as e:
        if e.errno == errno.WSAECONNRESET:
            print("connection closed")
            sys.exit()
        elif e.errno == errno.EWOULDBLOCK:
            pass
        else:
            return False, e
def sMsg(msg, channel): #send message
    try:
        headerLength = 10
        msg = msg.encode("utf-8")
        msgHeader = f"{len(msg) :< {headerLength}}".encode("utf-8")
        channelHeader = f"{len(channel) :< {headerLength}}".encode("utf-8")
        send = msgHeader + msg + channelHeader + channel
        sendHeader = f"{len(send):<{headerLength}}".encode("utf-8")
        clientSocket.send(sendHeader + send)
        return send
    except:
        return False
   
 
 
 
while True:
    msg = rMsg()
    if msg:
        print(msg)
    msg = input("> ")
    if msg:
        print("sent message: " + (sMsg(msg, channel)).decode("utf-8"))
