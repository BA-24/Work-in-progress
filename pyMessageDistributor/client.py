import socket
import select
import errno
import sys
import time

headerLength = 10
ip = "127.0.0.1"
port = 1194

blacklistedUsernames = ["False", "True"] #blacklisted usernames reserved to communicate to the client if the message received was handled correctly

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientSocket.connect((ip, port))
except ConnectionRefusedError:
    print('No connection found')
    sys.exit()
clientSocket.setblocking(False)
 
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

        if username in ["False", "True"]:
            return username, message
        return username, message
    except IOError as e:
        if e.errno == errno.WSAECONNRESET:
            print("connection to server closed.")
            sys.exit()
        elif e.errno == errno.EWOULDBLOCK:
            pass
        else:
            return False, e
    except ValueError:
        print("Message header was not received correctly.")
        return False
def sMsg(msg, channel): #send message
    headerLength = 10
    msg = msg.encode("utf-8")
    msgHeader = f"{len(msg) :< {headerLength}}".encode("utf-8")
    channelHeader = f"{len(channel) :< {headerLength}}".encode("utf-8")
    send = msgHeader + msg + channelHeader + channel
    sendHeader = f"{len(send):<{headerLength}}".encode("utf-8")
    clientSocket.send(sendHeader + send)
    for x in range(10):
        result = rMsg()
        if result == None:
            time.sleep(1)
        else:
            break
    if result == None:
        print("Server did not accept message.")
        return None
    elif result == False:
        print("Server did not return message received signal. Your message may not have been received.")
    elif result[0] == "False":
        print("Message returned False error, reason: " + result[1])
    elif result[0] == "True":
        if result[1] == msg.decode("utf-8"):
            print("Message was sent and received succesfully.")
        else:
            print("Message was received incorrectly, message received by server: " + result[1])
   

while True:
    username = input("Username: ")
    break
    if username in blacklistedUsernames:
        print("Your name is blacklisted. Please pick a different username")
    else:
        break
channel = input("Channel: ")
print("Connecting to server...")
username = username.encode("utf-8")
usernameHeader = f"{len(username):<{headerLength}}".encode("utf-8")
channel = channel.encode("utf-8")
channelHeader = f"{len(channel):<{headerLength}}".encode("utf-8")
send = usernameHeader + username + channelHeader + channel
sendHeader = f"{len(send):<{headerLength}}".encode("utf-8")

#clientSocket.send("bruh".encode("utf-8"))
clientSocket.send(sendHeader + send)
for x in range(10):
    result = rMsg()
    if result == None:
        time.sleep(1)
    else:
        break
if result == None:
    print("Server did not respond to user info.")
    sys.exit()
else:
    if result[0] == "False":
        print("Your connection was blocked by the server for the following reason: " + result[1])
        sys.exit()
    elif result[0] == username.decode("utf-8") and result[1] == channel.decode("utf-8"):
        print("Connection to server established")
    else:
        print("Your username or channel was not received correctly. Please try re-downloading the program or ask the server host about it.")
        sys.exit()
        

while True:
    msg = rMsg()
    if msg:
        print(msg)
    elif isinstance(msg, list) and msg[0] == "True":
        pass
    elif isinstance(msg, list) and msg[0] == "False":
        print("Unexpected error from server: " + msg[1])
    elif isinstance(msg, list) and msg[0] == False:
        print("Unexpected error: ")
        print(msg[1])
    msg = input("> ")
    if msg: sMsg(msg, channel)
