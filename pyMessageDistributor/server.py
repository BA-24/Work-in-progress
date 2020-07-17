import socket
import select
 
headerLength = 10
ip = "127.0.0.1"
port = 1194
 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((ip, port))
serverSocket.listen()
 
socketsList = [serverSocket]
clients = {}

blacklistedUsernames = ["False", "True"] #blacklisted usernames reserved to communicate to the client if the message received was handled correctly

def receiveMessage(clientSocket):
    try:
        messageHeader = int(clientSocket.recv(headerLength).decode("utf-8"))
        #print("primary header: " + str(messageHeader))
        message = clientSocket.recv(messageHeader)
        #print("primary message: " + str(message))
        message = message.decode("utf-8")
        header = message[0:headerLength]
        #print("secondary header: " + header)
        message = message.replace(header, "", 1)
        msg = message[0:int(header)]
        returnMsg = msg
        #print("secondary message: " + msg)
        message = message.replace(msg, "", 1)
        header = message[0:headerLength]
        #print("tertiary header: " + header)
        message = message.replace(header, "", 1)
        msg = message[0:int(header)]
        #print("tertiary message: " + msg)
        returnChannel = msg
        
        
        return [returnMsg, returnChannel]    
    except Exception as e:
        print("nerdinator: " + str(e))
        return False


while True:
    readSockets, _, exceptionSockets = select.select(socketsList, [], socketsList)
 
    for notifiedSocket in readSockets:
         
        if notifiedSocket == serverSocket:
            clientSocket, clientAddress = serverSocket.accept()
            user = receiveMessage(clientSocket)
            clients[clientSocket] = user
            if user != False and user[0] in ["False", "True"]:
                print('Rejected connection from {}:{}, username: {}, channel: {}'.format(*clientAddress, user[0], user[1]))
                msg = ["False"]
                msg+= ["Blacklistet username"]
                sendMsg = (f"{len(msg[0]):<{headerLength}}" + msg[0] + f"{len(msg[1]):<{headerLength}}" + msg[1]).encode("utf-8")
                clientSocket.send(sendMsg)
            else:
                if user is False:
                    continue
                socketsList.append(clientSocket)
                print('Accepted new connection from {}:{}, username: {}, channel: {}'.format(*clientAddress, user[0], user[1]))
                msg = f"{len(user[0]):<{headerLength}}".encode("utf-8") + user[0].encode("utf-8") + f"{len(user[1]):<{headerLength}}".encode("utf-8") + user[1].encode("utf-8")
                clientSocket.send(msg)
 
        else:
            message = receiveMessage(notifiedSocket)
 
            if message is False:
                print(f"Closed connection from {clients[notifiedSocket][0]}")
                socketsList.remove(notifiedSocket)
                del clients[notifiedSocket]
                continue
            user = clients[notifiedSocket]
            print(f"Received message from {user[0]} in {user[1]}: {message[0]}")
            returnMsg = f"{len('True'):<{headerLength}}".encode("utf-8") + "True".encode("utf-8") + f"{len('you are gay'):<{headerLength}}".encode("utf-8") + "you are gay".encode("utf-8")
            notifiedSocket.send(returnMsg)

            for clientSocket in clients:
                if clientSocket != notifiedSocket and clients[clientSocket][1] == clients[notifiedSocket][1]:
                    msg = f"{len(user[0]):<{headerLength}}".encode("utf-8") + user[0].encode("utf-8") + f"{len(message[0]):<{headerLength}}".encode("utf-8") + message[0].encode("utf-8")
                    clientSocket.send(msg)
 
 
        for notifiedSocket in exceptionSockets:
            socketsList.remove(notifiedSocket)
            del clients[notifiedSocket]
