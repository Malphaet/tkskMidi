base="""+--------------------------------------------------------------------------------------
| {title}
+--------------------------------------------------------------------------------------
| Main deck // {self.deck}
| Comunication arrays // {self.comms}
| {self.main_events}
+-----------------------------
| Inertia compensator // {self.inertia}
| Vital systems // {self.survival}
| {self.vital_events}
+-----------------------------
| Reactor status // {self.reactor}
| Reactor power // {self.reactor_pw}
| {self.reactor_events}
+-----------------------------
| Propultion status // {self.propulsion}
| Lightfold engines // {self.lightfold}
| Propultion power // {self.propulsion_pw}
| {self.prop_events}
+-----------------------------
| Docks // {self.docks}
| Medical Bay // {self.medical}
| Quarters // {self.quarters}
| Baracks // {self.baracks}
| {self.misc_events}
+--------------------------------------------------------------------------------------

+-----------------------------
| Users connected {users}
+--------------------------------------------------------------------------------------
"""


class messageStat():
    def __init__(self):
        self.cc=self.genall([16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,61,62],-1)
        self.note=self.genall([1,3, 4,6, 7,9, 10,12, 13,15, 16,18,19,21,22,24],0)
        # self.off=self.genempty([44])
        empty=lambda : ""
        align=11
        self.update()

    def pct(self,val):
        return int(val*100/127)

    def classical(self,val):
        pct=int(val*100/127)
        if val==-1:
            return "[--] {:>10}//red".format("Unknown")
        elif val==0:
            return "[{}%] {:>10}//red".format(pct,"Lost")
        elif val < 30:
            return "[{}%] {:>10}//red".format(pct,"Critical")
        elif val < 50:
            return "[{}%] {:>10}//borange".format(pct,"Warning")
        elif val < 80:
            return "[{}%] {:>10}//orange".format(pct,"Malfunction")
        elif val < 110:
            return "[{}%] {:>10}//green".format(pct,"Sub-Optimal")
        elif val < 127:
            return "[{}%] {:>10}//sblue".format(pct,"Nominal")
        elif val == 127:
            return "[{}%] {:>10}//bgreen".format(pct,"Optimal")

    def main_ev(self):
        ret=""
        if self.note[1]:
            ret+="Electrical surge ! "
        if self.note[3]:
            ret+="Uplink lost !"

        if ret != "":
            ret="Critical Issue//"+ret+"//bred"
        return ret

    def vital_ev(self):
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

    def reactor_ev(self):
        ret=""
        if self.note[7]:
            ret+="RADIATION LEAK ! "
            color="borange"
        if self.note[9]:
            ret+="REACTOR MELTDOWN ! "
            color="bred"
        if ret != "":
            ret="Critical Issue//"+ret+"//"+color
        return ret

    def prop_ev(self):
        ret=""
        if self.note[10]:
            ret+="System Overheating ! "
        if self.note[12]:
            ret+="Systemic Failure !"

        if ret != "":
            ret="Critical Issue//"+ret+"//bred"
        return ret

    def misc_ev(self):
        ret=""
        if self.note[13]:
            ret+="Electrical Fire ! "
        if self.note[15]:
            ret+=""

        if ret != "":
            ret="Critical Issue//"+ret+"//bred"
        return ret

    def update(self):
        self.deck=self.classical(self.cc[16])
        self.comms=self.classical(self.cc[17])

        self.inertia=self.classical(self.cc[20])
        self.survival=self.classical(self.cc[21])

        self.reactor=self.classical(self.cc[24])

        self.propulsion=self.classical(self.cc[28])
        self.lightfold=self.classical(self.cc[29])

        self.docks=self.classical(self.cc[46])
        self.medical=self.classical(self.cc[47])
        self.quarters=self.classical(self.cc[48])
        self.baracks=self.classical(self.cc[50])

        self.main_events=self.main_ev()
        self.vital_events=self.vital_ev()
        self.reactor_events=self.reactor_ev()
        self.prop_events=self.prop_ev()
        self.misc_events=self.misc_ev()

    def genall(self,t,val):
        content={}
        for nb in t:
            content[nb]=val
        return content



    def generateMessage(self,users=""):
        return base.format(title="I.S.F Esperance : Dashboard", self=self ,users=users)

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
        elif message.type=="note_on":
            print("off")
        self.update()

    def __str__(self):
        return self.generateMessage()

if __name__ == '__main__':
    print(messageStat().generateMessage("test"))
