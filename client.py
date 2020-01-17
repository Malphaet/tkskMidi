#!/bin/python3

# from tkinter import *
try:
    from tkinter import font
    import tkinter as tk
except:
    from Tkinter import font
    import Tkinter as tk
# from _thread import *
import threading,socket,time,sys,traceback
import config
from patch import decodehash
#################
# IMPORTANT INFO
FONT=config.FONT #"NovaMono"#'Speculum'
FONTSIZE=config.FONTSIZE
WIDTH=config.WIDTH
HEIGHT=config.HEIGHT
WINDOWSIZE=config.WINDOWSIZE
HOST,PORT=config.HOST,config.PORT
NAME=config.NAME
REFRESHINTERVAL=config.REFRESHINTERVAL

####################
# Quick and dirty code
root = tk.Tk()
root.title("Centauri Remote Viewer 1.0")
root.geometry(WINDOWSIZE)

main = font.Font(family=FONT, size=FONTSIZE)
# mainbold=font.Font(family=FONT, size=FONTSIZE, weight="bold")

font.families()

text = tk.Text(root,bg="black",font=main,padx=12,pady=12,cursor="cross",exportselection=0)
text.tag_config("default", background="black", foreground="green")

text.tag_config("bred", background="red", foreground="black")
text.tag_config("red", background="black", foreground="red")

text.tag_config("bgreen", background="green", foreground="black")
text.tag_config("green", background="black", foreground="green")

text.tag_config("blue", background="black", foreground="blue")
text.tag_config("bblue", background="blue", foreground="black")

text.tag_config("sblue", background="black", foreground="SteelBlue")
text.tag_config("bsblue", background="SteelBlue", foreground="black")

text.tag_config("rblue", background="black", foreground="RoyalBlue4")
text.tag_config("brblue", background="RoyalBlue4", foreground="black")

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

def newtext(text,lines):
    text.delete("1.0",tk.END)
    for l in range(lines):
        text.insert(tk.INSERT,"\n")
newtext(text,HEIGHT)

def exit(event=None):
    quit()

def insertt(text,message,tag):
    try:
        text._tobewritten+=[(message,tag)]
        # text.insert(tk.INSERT,message,tag)
    except:
        print(criticalTraceback())#tpass
        exit()

def writeall(text):
    try:
        start_time = time.time()
        text.delete("1.0","1.end")
        text.mark_set(tk.INSERT,"1.0")
        l=1

        for line in text._tobewritten:
            if line[0]==0:
                l+=1
                text.mark_set(tk.INSERT,str(l)+".0")
                text.delete(tk.INSERT,"insert lineend")
                # time.sleep(0.025)
            else:
                text.insert(tk.INSERT,line[0],line[1])
        # print(" Written {} lines in {} seconds".format(len(text._tobewritten),time.time()-start_time))
        text._tobewritten=[]
    except ValueError:
        print(trackme())
        text._tobewritten=[]

colors={"g":"green","G":"bgreen","r":"red","R":"bred","u":"blue","U":"bblue","s":"sblue","S":"bsblue","l":"lgreen","L":"blgreen","o":'orange','O':"borange","y":"rblue","Y":"brblue"}
def colorform(col):
    try:
        return colors[col]
    except IndexError:
        print(trackme())
        return "default"

def plain(text,msg,style="default"):
    insertt(text,msg,style)
    insertt(text,0,"default")

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
    insertt(text,0,"default")

def splittank(tankt):
    tanks,nb=[],0
    for tank in tankt: # Split label:value
        label,rpct,colt,coll=tank.split(":")
        pct=int(int(rpct)*5/100)
        try:
            col=ctanks[pct]
        except ValueError:
            print(trackme())
            col="bred"
        tanks+=[(label,pct,col,rpct,colt,coll)]
        #size=max(size,len(label))
        nb+=1
    return tanks,nb

ctanks=["bred","borange","bgold","bsblue","brblue","bgreen","bred"]
def tanks(text,msgtotal,colortitle):
    tankt=msgtotal.split("//") # Split all tank
    size=4
    f="{:^7}" # +3 because of the len("+=+")
    #f="{:^"+str(size+3)+"}"
    tanks,nb=splittank(tankt)

    #Building all tanks
    pad=" "*int(size/2)
    sepline=(pad+"+=+"+pad)*nb
    insertt(text,sepline,colortitle)
    insertt(text,0,colortitle)
    for line in range(5): #build all tanks line by line
        for tank in tanks:
            if tank[1]>4-line:
                insertt(text,pad+'|',colortitle)
                insertt(text,'#',tank[4])#tank[2])
                insertt(text,'|'+pad,colortitle)
            else:
                insertt(text,pad+'| |'+pad,colortitle)
        insertt(text,0,colortitle)
    insertt(text,sepline,colortitle)
    insertt(text,0,colortitle)
    for tank in tanks:
        insertt(text,f.format(tank[0][:size+3]),tank[5])
    insertt(text,0,colortitle)
    for tank in tanks:
        insertt(text,f.format(tank[3]+"%"),tank[2])
    insertt(text,0,colortitle)

def minitanks(msgtotal):
    tankt=msgtotal.split("//")
    pass

def multipercent(msg):
    "&color title of section // subsection:percent // subsection:percent ..."
    pass

def superstyle(text,msg):
    if msg[0]=="!": #Oneline colorcoded
        plain(text,msg[2:],colorform(msg[1]))
    elif msg[0]=="@":
        tanks(text,msg[2:],colorform(msg[1]))
    elif msg[0]=="#": # Filled line
        filled(text,msg[2:],colorform(msg[1]))
    else:
        plain(text,msg,"default")

def receive(message_rcv,text):
    text._tobewritten=[]
    for line in message_rcv.splitlines():
        try:
            superstyle(text,line)
        except (IndexError,ValueError): # Second is for split on tanks, custom error is likely better
            # print(trackme())
            if len(line)>2:
                line=line[2:]
            insertt(text,line,"default")
            insertt(text,0,"default")
    try:
        text.config(state=tk.NORMAL) #Acquire lock
        writeall(text)
        text.config(state=tk.DISABLED)
    except RuntimeError:
        print("Forcibly exiting...")
        exit()

def connecting():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def criticalTraceback():
    exc,funct,tb=sys.exc_info()
    code=tb.tb_frame.f_code
    # traceback.print_exception(exc,funct,tb)
    print(traceback.format_exc())
    print("---")
    traceback.print_exc()
    return("[Critical error] {} line {} ({}@{})".format(exc.__name__,code.co_firstlineno,code.co_name,code.co_filename))

def trackme():
    import inspect
    print(inspect.currentframe().f_back)

def threadclient():
    global s
    receive(messages.opening_text0,text)
    tryouts=0
    oldhash=""
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
        time.sleep(2)
        try:
            s.send(bytes("{}".format(NAME),'UTF-8'))
        except (BrokenPipeError,OSError):
            receive(messages.handshake_error,text)
            time.sleep(2)
            continue#exit()

        while 1:
            try:
                data=s.recv(2048)
                newhash,data=decodehash(data)
                if newhash==oldhash:
                    continue
                oldhash=newhash
                if data!=0:
                    msg=str(data.decode('UTF-8'))
                    receive(str(data.decode('UTF-8')),text)
                else:
                    break
                time.sleep(0.01)
            except ConnectionResetError:
                trackme()
                s.close()
                receive(messages.connection_terminated,text)
                receive(messages.retrying_connection,text)
                tryouts=0
                break
            except OSError:
                exit()
            except Exception as e:
                print(trackme())
                print(criticalTraceback())
################
# SYSTEM MESSAGE

import messages

if __name__ == '__main__':
    s=None
    thread=threading.Thread(target=threadclient,args=())
    thread.start()
    def on_closing(*args):
        root.destroy()
        try:
            s.close()
            thread.join()
        except:
            pass
        exit()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.bind('<Control-q>', on_closing)
    root.bind('<Control-c>', on_closing)
    root.mainloop()
    exit()
