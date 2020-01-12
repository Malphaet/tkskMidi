base="""+---------------------------------------------------------------------------
| {title}
+---------------------------------------------------------------------------
| Main deck // {self.deck}
| Comunication arrays // {self.comms}
| {self.main_events}
+-----------------------------
| Inertia compensator // {self.inertia}
| Vital systems // {self.survival}
| {self.vital_events}
+-----------------------------
| Reactor status // {self.reactor}
| {self.reactor_events}
+-----------------------------
| Propultion status // {self.propulsion}
| Lightfold engines // {self.lightfold}
+-----------------------------
| Docks // {self.docks}
| Medical Bay // {self.medical}
| Quarters // {self.quarters}
| Baracks // {self.baracks}
| {self.misc_events}
+---------------------------------------------------------------------------

+-----------------------------
| Users connected {users}
+---------------------------------------------------------------------------
"""


class messageStat():
    def __init__(self):
        self.cc=self.genall([16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,61,62],-1)
        self.note=self.genall([1,3, 4,6, 7,9, 10,12, 13,15, 16,18,19,21,22,24],0)
        # self.off=self.genempty([44])
        empty=lambda : ""

        self.update()

    def pct(self,val):
        return int(val*100/127)

    def classical(self,val):
        pct=int(val*100/127)
        if val==-1:
            return "[--] Unknown//red".format(pct)
        elif val==0:
            return "[{}%] Lost//red".format(pct)
        elif val < 30:
            return "[{}%] Critical//red".format(pct)
        elif val < 50:
            return "[{}%] Warning//borange".format(pct)
        elif val < 80:
            return "[{}%] Malfunction//orange".format(pct)
        elif val < 110:
            return "[{}%] Sub-Optimal//green".format(pct)
        elif val < 127:
            return "[{}%] Nominal//bblue".format(pct)
        elif val == 127:
            return "[{}%] Optimal//bgreen".format(pct)

    def reactor_ev(self):
        ret=""
        if self.note[7]:
            ret+="REACTOR MELTDOWN "
        if self.note[9]:
            ret+="RADIATION LEAK "

        if ret != "":
            ret="CRITICAL ISSUE//"+ret+"//bred"
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

        self.main_events=""
        self.vital_events=""
        self.reactor_events=self.reactor_ev()
        self.misc_events=""

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
