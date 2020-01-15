MIDINAMEIN='Virtual Port 2'
import mido,sys

import time
import rtmidi

try:
    interface=mido.open_output(MIDINAMEIN)
except OSError:
    print("  Could not open interface {}, available are : {}".format(MIDINAMEIN,mido.get_output_names()))
    exit()
message_type={"n":"note_on","note":"note_on","on":"note_on","cc":"control_change","ch":"control_change"}

cc_test=[16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62]
note_test=[1,3, 4,6, 7,9, 10,12, 13,15, 16,18,19,21,22,24]

def parsemsg(msg):
    msg=msg.strip(" ")
    msg_sp=msg.split(" ")

    ty=msg_sp[0].strip(" ")
    ty=message_type[ty]

    chan=int(msg_sp[1])

    if len(msg_sp)<3:
        val=127
    else:
        val=int(msg_sp[2])

    if ty=="control_change":
        msg=interface.send(mido.Message(ty,control=chan,value=val))
    elif ty=="note_on":
        msg=interface.send(mido.Message(ty,note=chan,velocity=val))

def loop():
    print("> Send midi message on interface [{}]".format(MIDINAMEIN))
    print("> Format is message=(cc/on) (note/channel) (value) / <message>\n")
    while True:
        try:
            msg=input("Enter message to send : ")
            msglist=msg.split("/")
            for msg in msglist:
                parsemsg(msg)
        except KeyError:
            print("  Key not recognised {}".format(ty))
        except ValueError:
            print("  Input [{}] is ill formated".format(msg))
        except KeyboardInterrupt:
            print("  Exiting")
            exit()

if __name__ == '__main__':
    if(len(sys.argv)>1):
        if sys.argv[1]in("interactive","i"):
            loop()
    else:
        import time
        from random import randint
        print("Sending all notes")
        for i in range(4):
            for m in note_test:
                parsemsg("note {}".format(m))
            time.sleep(2)
        print("Sending all control_change")
        for i in range(22):
            for m in cc_test:
                cmd="cc {} {}".format(m,min(i*6+randint(1,7),127))
                parsemsg(cmd)
            time.sleep(1)
