#!/bin/python3
import threading,socket,time
import messages

SLEEP_SCHEDULER=0.5
global_status=messages.global_status[:]

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    def run(self):
        # Getting basic information, mainly name
        print ("Connection from : ", clientAddress)
        data = self.csocket.recv(2048)
        name = data.decode()
        print ("{} connected @ {} ".format(name,clientAddress))
        self.csocket.send(bytes(messages.handshake.format(name),'UTF-8'))

        while True:
            try:
                time.sleep(SLEEP_SCHEDULER)
                self.csocket.send(bytes(global_status,'UTF-8'))
            except ConnectionResetError:
                print (name, clientAddress , " disconnected...")
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
