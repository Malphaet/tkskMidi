#!/bin/python3
import threading,socket,time
import patch,messages
import mido

SLEEP_SCHEDULER=1
HOST = "127.0.0.1"
PORT = 12345
MIDINAME='MIDI Mix 0'

global_users=set()
global_status=patch.messageStat()

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
        global_users.add(name)
        print("Connected users",global_users)
        self.csocket.send(bytes(messages.handshake.format(name),'UTF-8'))

        while True:
            try:
                time.sleep(SLEEP_SCHEDULER)
                self.csocket.send(bytes(str(global_status.generateMessage(global_users)),'UTF-8'))
            except ConnectionResetError:
                try:
                    global_users.remove(name)
                except:
                    pass
                print (name, clientAddress , " disconnected...")
                print ("Connected users",global_users)
                break


class MidiThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        try:
            self.interface=mido.open_input(name)
        except:
            print("[ERROR] Impossible to open input {} (available are {})".format(name,mido.get_input_names()))
            exit()
        print ("Started the midi interface")

    def run(self):
        for msg in self.interface:
            global_status.updateMessage(msg)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))


print("Server started")
print("Waiting for client request..")

inter=MidiThread(MIDINAME)
inter.start()

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
