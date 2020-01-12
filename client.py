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
FONTSIZE=18
WIDTH=85
WINDOWSIZE="1250x800"
HOST,PORT=("192.168.1.13",12345)
NAME="Aamstrang Karpov"
####################
# Quick and dirty code
root = tk.Tk()
root.title("Centauri Remote Viewer 0.9")
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
        text.insert(tk.INSERT,message,tag)
    except:
        pass


def superstyle(text):
    try:
        if text[0]=="!":
            return "red"
        elif text[0]==".":
            return "orange"
        return "default"
    except:
        return "default"

def receive(message_rcv,text):
    try:
        text.config(state=tk.NORMAL)
        text.delete("1.0",tk.END)
    except RuntimeError:
        print("Forcibly exiting...")
        exit()
    # k=0
    for line in message_rcv.splitlines():
        # k+=1
        try:
            # text.delete("{}.0".format(k),"{}.end".format(k))#"{}.first".format(k),"{}.last".format(k))#tk.END)
            messaget=line.split("//")
            msg=messaget[0].strip(" ")
            info=messaget[1].strip(" ")
            remaining=max(0,WIDTH-len(msg)-len(info))
            if len(messaget)==3:
                style=messaget[2]
            elif len(messaget)==2:
                style="default"
            insertt(text,msg,superstyle(msg))
            insertt(text," "+"."*remaining+" ","default")
            insertt(text,info,style)
            insertt(text,"\n","default")
        except:
            insertt(text,line,superstyle(line))
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
    except (BrokenPipeError,OSError):
        receive(messages.handshake_error,text)
        time.sleep(1)
        exit()

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
