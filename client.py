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

#################
# IMPORTANT INFO
FONT="White Rabbit"#"NovaMono"#'Speculum'
FONTSIZE=19
WIDTH=85
WINDOWSIZE="1250x800"
HOST,PORT=("127.0.0.1",12345)
NAME="Aamstrang Karpov"
####################
# Quick and dirty code
root = tk.Tk()
root.title("Centauri Remote Viewer 0.9")
root.geometry("1300x600")
root.bind('<Control-q>', exit)
root.bind('<Control-c>', exit)

main = font.Font(family=FONT, size=FONTSIZE)
# mainbold=font.Font(family=FONT, size=FONTSIZE, weight="bold")

font.families()

text = tk.Text(root,bg="black",font=main,padx=12,pady=12,cursor="trek")
text.tag_config("default", background="black", foreground="green")
text.tag_config("info", background="black", foreground="green")
text.tag_config("red", background="red", foreground="black")
text.tag_config("green", background="green", foreground="black")
text.tag_config("warning", background="black", foreground="orange")

text.tag_config("title", background="black", foreground="green")#,font=mainbold)


text.pack(fill=tk.BOTH,expand=1)

def exit(event=None):
    quit()

def insertt(text,message,tag):
    try:
        text.insert(tk.END,message,tag)
    except:
        pass


def receive(message_rcv,text):
    try:
        text.config(state=tk.NORMAL)
        text.delete("1.0",tk.END)
    except RuntimeError:
        print("Forcibly exiting...")
        exit()
    for line in message_rcv.splitlines():
        try:
            messaget=line.split("//")
            msg=messaget[0].strip(" ")
            info=messaget[1].strip(" ")
            remaining=max(0,WIDTH-len(msg)-len(info))
            if len(messaget)==3:
                style=messaget[2]
            elif len(messaget)==2:
                style="default"
            insertt(text,msg,"title")
            insertt(text," "+"."*remaining+" ","default")
            insertt(text,info,style)
            insertt(text,"\n","default")
        except:
            insertt(text,line,"info")
            insertt(text,"\n","default")
    text.config(state=tk.DISABLED)


def threadclient():
    time.sleep(1)
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        receive(messages.connection_error,text)
    receive(messages.connected,text)
    try:
        s.send(bytes("{}".format(NAME),'UTF-8'))
    except BrokenPipeError:
        receive(messages.handshake_error,text)
        time.sleep(1)
        exit()

    while 1:
        try:
            data=s.recv(1024)
            if data!=0:
                receive(str(data.decode('UTF-8')),text)
            else:
                break
        except ConnectionResetError:
            s.close()
            receive(messages.connection_terminated,text)
            break
################
# SYSTEM MESSAGE

import messages

message_test2="""Nope"""
if __name__ == '__main__':
    receive(messages.opening_text0,text)
    thread=threading.Thread(target=threadclient,args=())
    thread.start()

    root.mainloop()
    exit()
