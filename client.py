#!/bin/python3

# from tkinter import *
try:
    from tkinter import font
    import tkinter as tk
except:
    from Tkinter import font
    import Tkinter as tk
# from _thread import *
import threading,socket,time
import config

#################
# IMPORTANT INFO
FONT=config.FONT #"NovaMono"#'Speculum'
FONTSIZE=config.FONTSIZE
WIDTH=config.WIDTH
WINDOWSIZE=config.WINDOWSIZE
HOST,PORT=config.HOST,config.PORT
NAME=config.NAME
####################
# Quick and dirty code
root = tk.Tk()
root.title("Centauri Remote Viewer 1.0")
root.geometry(WINDOWSIZE)
root.bind('<Control-q>', exit)
root.bind('<Control-c>', exit)

main = font.Font(family=FONT, size=FONTSIZE)
# mainbold=font.Font(family=FONT, size=FONTSIZE, weight="bold")

font.families()

text = tk.Text(root,bg="black",font=main,padx=12,pady=12,cursor="cross")
text.tag_config("default", background="black", foreground="green")

text.tag_config("bred", background="red", foreground="black")
text.tag_config("red", background="black", foreground="red")

text.tag_config("bgreen", background="green", foreground="black")
text.tag_config("green", background="black", foreground="green")

text.tag_config("blue", background="black", foreground="blue")
text.tag_config("bblue", background="blue", foreground="black")

text.tag_config("sblue", background="black", foreground="SteelBlue")
text.tag_config("bsblue", background="SteelBlue", foreground="black")

text.tag_config("dgreen", background="black", foreground="dark green")
text.tag_config("bdgreen", background="dark green", foreground="black")

text.tag_config("lgreen", background="black", foreground="lawn green")
text.tag_config("blgreen", background="lawn green", foreground="black")

text.tag_config("gold", background="black", foreground="gold")
text.tag_config("bgold", background="gold", foreground="black")

text.tag_config("orange", background="black", foreground="orange")
text.tag_config("borange", background="orange", foreground="black")

text.tag_config("title", background="black", foreground="green")#,font=mainbold)


text.pack(fill=tk.BOTH,expand=1)

def exit(event=None):
    quit()

def insertt(text,message,tag):
    try:
        text._tobewritten+=[(message,tag)]
        # text.insert(tk.INSERT,message,tag)
    except:
        pass

def writeall(text):
    try:
        for line in text._tobewritten:
            text.insert(tk.INSERT,line[0],line[1])
        text._tobewritten=[]
        #Release lock
    except:
        text._tobewritten=[]

colors={"g":"green","G":"bgreen","r":"red","R":"bred","u":"blue","U":"bblue","s":"sblue","S":"bsblue","l":"lgreen","L":"blgreen","o":'orange','O':"borange"}
def colorform(col):
    try:
        return colors[col]
    except:
        return "default"

def plain(text,msg,style="default"):
    insertt(text,msg,style)
    insertt(text,"\n","default")

def filled(text,msgtotal,colortitle):
    messaget=msgtotal.split("//")
    msg=messaget[0].strip(" ")
    info=messaget[1].strip(" ")
    remaining=max(0,WIDTH-len(msg)-len(info))
    stylet="default"
    if len(messaget)==3:
        style=messaget[2]
    elif len(messaget)==2:
        style="default"
    insertt(text,msg,colortitle)
    insertt(text," "+"."*remaining+" ","default")
    insertt(text,info,style)
    insertt(text,"\n","default")

def superstyle(text,msg):
    if msg[0]=="!": #Oneline colorcoded
        plain(text,msg[2:],colorform(msg[1]))
    # elif text[0]==".":
    #     return "orange",text[1:]
    elif msg[0]=="#": # Filled line
        filled(text,msg[2:],colorform(msg[1]))
    else:
        plain(text,msg,"default")

def receive(message_rcv,text):
    text._tobewritten=[]
    
    for line in message_rcv.splitlines():
        try:
            superstyle(text,line)
        except:
            if len(line)>2:
                line=line[2:]
            insertt(text,line,"default")
            insertt(text,"\n","default")
    try:
        text.config(state=tk.NORMAL) #Acquire lock
        text.delete("1.0",tk.END)
        writeall(text)
        text.config(state=tk.DISABLED)
    except RuntimeError:
        print("Forcibly exiting...")
        exit()

def connecting():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def threadclient():
    receive(messages.opening_text0,text)
    tryouts=0
    while 1: # Main connection loop
        time.sleep(1)
        s=connecting()
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            tryouts+=1
            receive(messages.connection_error.format(tnumber=tryouts,tcolor="orange"),text)
            time.sleep(2)
            continue
        receive(messages.connected,text)
        try:
            s.send(bytes("{}".format(NAME),'UTF-8'))
        except (BrokenPipeError,OSError):
            receive(messages.handshake_error,text)
            time.sleep(3)
            continue#exit()

        while 1:
            try:
                data=s.recv(2048)
                if data!=0:
                    receive(str(data.decode('UTF-8')),text)
                else:
                    break
            except ConnectionResetError:
                s.close()
                receive(messages.connection_terminated,text)
                receive(messages.retrying_connection,text)
                tryouts=0
                break
################
# SYSTEM MESSAGE

import messages

if __name__ == '__main__':
    thread=threading.Thread(target=threadclient,args=())
    thread.start()
    root.mainloop()
    exit()
