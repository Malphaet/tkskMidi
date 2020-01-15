#!/bin/python3
import threading,socket,time,hashlib
import patch,messages
import mido
import config

SLEEP_SCHEDULER=config.SLEEP_SCHEDULER
HOST = config.SERVERNAME
PORT = config.SERVERPORT
MIDINAME=config.MIDINAME

global_users={}
global_status=patch.messageStat()
# writelock=threading.Lock()

def showusers():
    ret=""
    for user in global_users:
        if global_users[user]>0:
            ret+=" "+user
    return ret

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket

    def send(self,msg):
        # msg=msg.encode('UTF-8')
        # msg=self.hashit(msg)+msg # It is grossly inneficient to do it that way, hash should be prerendered with a _hash attribute
        self.csocket.send(bytes(msg,'UTF-8'))

    def run(self):
        # Getting basic information, mainly name
        data = self.csocket.recv(2048)
        name = data.decode()
        print ("[{}] {} connected @ {} ".format(time.strftime("%X"),name,clientAddress))
        try:
            global_users[name]+=1
        except:
            global_users[name]=1
        print("[Users] : ",showusers())
        global_status.updadeMessage(showusers())
        self.send(messages.handshake.format(name))
        time.sleep(0.2)
        while True:
            try:
                self.send(global_status.message())
                time.sleep(SLEEP_SCHEDULER)
            except (ConnectionResetError,ConnectionAbortedError):
                try:
                    global_users[name]-=1
                    if global_users[name]<0:
                        global_users[name]=0 # Could also drop entry
                except:
                    pass
                print ("[{}] {}@{} disconnected".format(time.strftime("%X"),name, clientAddress))
                print ("[Users] : ",showusers())
                global_status.updadeMessage(showusers())
                break


class MidiThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        try:
            self.interface=mido.open_input(name)
        except:
            print("[ERROR] Impossible to open input {} (available are {})".format(name,mido.get_input_names()))
            exit()
        print ("[INFO] Midi interface status .. Started")

    def run(self):
        for msg in self.interface:
            # print(msg) # For debug purposes
            global_status.updateMessage(msg)
            global_status.updadeMessage(showusers())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))


print("[INFO] Server status .......... Started")

inter=MidiThread(MIDINAME)
inter.start()

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
