base="""!g+--------------------------------------------------------------------------------------
!g| {title}
!g+--------------------------------------------------------------------------------------
#g| Global communication array // {self.comm}
#g| {self.comm_events}
!g+-----------------------------
#g| Mothership Integrity // {self.integrity}
#g| Mothership Ammunition // {self.ammu}
#g| {self.mothership_events}
!g+-----------------------------
#g| Target 1 // {self.t1}
#g| Target 2 // {self.t2}
#g| Target 3 // {self.t3}
#g| Target 4 // {self.t4}
#g| Target 5 // {self.t5}
#g| Target 6 // {self.t6}
#g| {self.target_events}
!g+--------------------------------------------------------------------------------------

!g                                 Squad One
@g {self.acc}

&y {self.hull}
&y {self.ammo}

!g+-----------------------------
#g| Users connected {users}
!g+--------------------------------------------------------------------------------------
"""

import hashlib

def hashmsg(text):
    "Return a :6 hex hash"
    h = hashlib.md5(text.encode("utf-8"))
    return(h.hexdigest()[:7])


def check(text,md5):
    "Check message integrity"
    return md5==hashmsg(text)

def decodehash(text):
    "Return hash, msg"
    return text[:7],text[7:]

def encodehash(text):
    "Return hash+msg"
    return hashmsg(text)+text

class messageStat():
    def __init__(self):
        self.cc=self.genall([16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62],-1)
        self.note=self.genall([1,3, 4,6, 7,9, 10,12, 13,15, 16,18,19,21,22,24],0)
        # self.off=self.genempty([44])
        empty=lambda : ""
        align=11
        self.update()
        self._message=""
        self._hash=hashmsg(self._message)

    def pct(self,val):
        return int(val*100/127)

    def classical(self,val):
        pct=int(val*100/127)
        if val==-1:
            return "[--] {:>11}//red".format("Unknown")
        elif val==0:
            return "[{:>2}%] {:>11}//red".format(pct,"Lost")
        elif val < 30:
            return "[{:>2}%] {:>11}//red".format(pct,"Critical")
        elif val < 50:
            return "[{:>2}%] {:>11}//borange".format(pct,"Warning")
        elif val < 80:
            return "[{:>2}%] {:>11}//orange".format(pct,"Malfunction")
        elif val < 110:
            return "[{:>2}%] {:>11}//green".format(pct,"Sub-Optimal")
        elif val < 127:
            return "[{:>2}%] {:>11}//sblue".format(pct,"Nominal")
        elif val == 127:
            return "[{:>2}%] {:>11}//bgreen".format(pct,"Optimal")

    def powerlevel(self,val):
        pct=int(val*2)
        if val==-1:
            return "[--%]//red".format(pct)
        if pct < 50:
            return "[{:>2}%]//sblue".format(pct)
        if pct < 105:
            return "[{:>2}%]//green".format(pct)
        if pct < 175:
            return "[{:>2}%]//orange".format(pct)
        if pct < 200:
            return "[{:>2}%]//red".format(pct)
        return "[{:>2}%]//bred".format(pct)

    def acc_ev(self):
        return "Acc1:{}:bgold:gold // Acc2:{}:bgold:gold // Acc3:{}:bgold:gold // Acc4:{}:bgold:gold // Acc5:{}:bgold:gold // Acc6:{}:bgold:gold".format(
        self.cc[28],self.cc[29],self.cc[30], # Oxy
        self.cc[46],self.cc[47],self.cc[48]) # Acc

    def hull_ev(self):
        return "Hull integrity // :{}// :{}// :{}// :{}// :{}// :{}".format(
            self.cc[50],self.cc[51],self.cc[52],self.cc[54],self.cc[55],self.cc[56]) # Shielding

    def ammo_ev(self):
        return "Ammunition // :{}// :{}// :{}// :{}// :{}// :{}".format(
            self.cc[19],self.cc[23],self.cc[27],self.cc[31],self.cc[49],self.cc[53]) # Shielding

    def comm_ev(self):
        ret=""
        if self.note[1]:
            ret+="Electrical surge ! "
        if self.note[3]:
            ret+="Uplink lost !"

        if ret != "":
            ret="Critical Issue//"+ret+"//bred"
        return ret

    def mothership_ev(self):
        ret=""
        if self.note[4]:
            ret+="Microgravity Malfunction ! "
            color="borange"
        if self.note[6]:
            ret+="Oxygen Leak !"
            color="bred"
        if ret != "":
            ret="Critical Issue//"+ret+"//"+color
        return ret

    def target_ev(self):
        ret=""
        if self.note[7]:
            ret+="Target class unknown "
            color="borange"
        if self.note[9]:
            ret+="Target lost "
            color="bred"
        if ret != "":
            ret="Critical Issue//"+ret+"//"+color
        return ret

    def update(self):
        self.comm=self.classical(self.cc[16])

        self.integrity=self.classical(self.cc[17])
        self.ammu=self.powerlevel(self.cc[18])

        self.t1=self.powerlevel(self.cc[20])
        self.t2=self.powerlevel(self.cc[21])
        self.t3=self.powerlevel(self.cc[22])
        self.t4=self.powerlevel(self.cc[24])
        self.t5=self.powerlevel(self.cc[25])
        self.t6=self.powerlevel(self.cc[26])

        self.mothership_events=self.mothership_ev()
        self.comm_events=self.comm_ev()
        self.target_events=self.target_ev()

        self.acc=self.acc_ev()
        # self.smalltanks=self.smalltanks_ev()
        self.hull=self.hull_ev()
        self.ammo=self.ammo_ev()

    def genall(self,t,val):
        content={}
        for nb in t:
            content[nb]=val
        return content

    def hmessage(self):
        return self._hmessage
    def message(self):
        return self._message
    def __str__(self):
        return self._message

    def updadeMessage(self,users=""):
        self._message=base.format(title="C.L.S Strike Squad One : Dashboard", self=self ,users=users)
        self._hash=hashmsg(self._message)
        self._hmessage=self._hash+self._message
        return self._message

    def updateMessage(self,message):
        # print(message)
        if message.type=="control_change":
            try:
                self.cc[message.control]=message.value
            except:
                pass
        elif message.type=="note_on":
            try:
                if self.note[message.note]:
                    self.note[message.note]=0
                else:
                    self.note[message.note]=1
                # print (self.note)
            except:
                pass
        # elif message.type=="note_off":
        #     print("off")
        self.update()

if __name__ == '__main__':
    print(messageStat().updadeMessage("test"))
