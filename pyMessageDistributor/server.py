import socket
import select
 
headerLength = 10
ip = "192.168.1.240"
port = 2
 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((ip, port))
serverSocket.listen()
 
socketsList = [serverSocket]
clients = {}


def receiveMessage(clientSocket):
    try:
        print("running receiveMessage")
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
        print("secondary message: " + msg)
        message = message.replace(msg, "", 1)
        header = message[0:headerLength]
        #print("tertiary header: " + header)
        message = message.replace(header, "", 1)
        msg = message[0:int(header)]
        print("tertiary message: " + msg)
        returnChannel = msg
        
        
        return [returnMsg, returnChannel]    
 
    except Exception as e:
        print("nerdinator: " + str(e))
        return False
 
 
while True:
    print("running loop")
    readSockets, _, exceptionSockets = select.select(socketsList, [], socketsList)
 
    for notifiedSocket in readSockets:
         
        if notifiedSocket == serverSocket:
            clientSocket, clientAddress = serverSocket.accept()
            user = receiveMessage(clientSocket)
            if user is False:
                continue
            socketsList.append(clientSocket)
            clients[clientSocket] = user
            print('Accepted new connection from {}:{}, username: {}, channel: {}'.format(*clientAddress, user[0], user[1]))
 
        else:
            print("old socket found")
            message = receiveMessage(notifiedSocket)
 
            if message is False:
                print(f"Closed connection from {clients[notifiedSocket][0]}")
                socketsList.remove(notifiedSocket)
                del clients[notifiedSocket]
                continue
            user = clients[notifiedSocket]
            print(f"Received message from {user[0]} in {user[1]}: {message[0]}")

            for clientSocket in clients:
                print(clients[notifiedSocket][1])
                if clientSocket != notifiedSocket and clients[clientSocket][1] == clients[notifiedSocket][1]:
                    msg = f"{len(user[0]):<{headerLength}}".encode("utf-8") + user[0].encode("utf-8") + f"{len(message[0]):<{headerLength}}".encode("utf-8") + message[0].encode("utf-8")
                    print(msg)
                    clientSocket.send(msg)
 
 
        for notifiedSocket in exceptionSockets:
            socketsList.remove(notifiedSocket)
            del clients[notifiedSocket]
