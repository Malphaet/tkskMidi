#!/bin/python3
import threading,socket,time

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    def run(self):
        # Getting basic information, mainly name
        print ("Connection from : ", clientAddress)
        data = self.csocket.recv(2048)
        msg = data.decode()
        name=data.lowercase()
        print ("Connection from : ", clientAddress,name)

        k=1
        while True:
            try:
                time.sleep(1)
                self.csocket.send(bytes("{}".format(k),'UTF-8'))
                k+=1
            except ConnectionResetError:
                print ("Client at ", clientAddress , " disconnected...")
                break
LOCALHOST = "127.0.0.1"
PORT = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
