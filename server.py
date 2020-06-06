#!/bin/python3
import threading,socket,time
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
            ret+=" / "+user
    return ret

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.keepalive=True

    def send(self,msg):
        # msg=msg.encode('UTF-8')
        self.csocket.send(bytes(msg,'UTF-8'))

    def run(self):
        global global_users
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
        self.send(patch.encodehash(messages.handshake.format(name))) # if errror here the user cound isn't diminished
        time.sleep(0.2)
        while self.keepalive:
            try:
                self.send(global_status.hmessage())
                time.sleep(SLEEP_SCHEDULER)
            except (ConnectionResetError,ConnectionAbortedError,BrokenPipeError):
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
            #print(msg) # For debug purposes
            global_status.updateMessage(msg)
            global_status.updadeMessage(showusers())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))


print("[INFO] Server status .......... Started")

inter=MidiThread(MIDINAME)
inter.start()

while True:
    try:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()
    except KeyboardInterrupt:
        exit() # Clearly not working
