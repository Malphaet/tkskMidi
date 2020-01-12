base="""+-------------------------------------------------------
| {title}
+-------------------------------------------------------
| Main deck // {self.deck}
| Comunication arrays // {self.comms}
| {self.main_events}
+-----------------
| Inertia compensator // {self.inertia}
| Vital systems // {self.survival}
| {self.vital_events}
+-----------------
| Reactor status // {self.reactor}
| {self.reactor_events}
+-----------------
| Propultion status // {self.propulsion}
| Lightfold engines // {self.lightfold}
+-----------------
| Docks // {self.docks}
| Medical Bay // {self.medical}
| Quarters // {self.quarters}
| Baracks // {self.baracks}
| {self.misc_events}
+-------------------------------------------------------

+----
| Users connected {users}
+-------------------------------------------------------
"""


class messageStat():
    def __init__(self):
        self.cc=self.genempty([16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,61,62])
        self.on=self.genempty([44])
        self.off=self.genempty([44])
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
            return "[{}%] Warning//bigwarning".format(pct)
        elif val < 80:
            return "[{}%] Malfunction//warning".format(pct)
        elif val < 110:
            return "[{}%] Sub-Optimal//green".format(pct)
        elif val < 127:
            return "[{}%] Nominal//blue".format(pct)
        elif val == 127:
            return "[{}%] Optimal//green".format(pct)

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

        self.vital_events=""
        self.reactor_events=""
        self.main_events=""
        self.misc_events=""

    def genempty(self,t):
        content={}
        for nb in t:
            content[nb]=-1
        return content


    def generateMessage(self,users=""):
        return base.format(title="I.S.F Espérance : Dashboard", self=self ,users=users)

    def updateMessage(self,message):
        print(message)
        if message.type=="control_change":
            try:
                self.cc[message.control]=message.value
            except:
                pass
        elif message.type=="note_on":
            print("on")
        elif message.type=="note_on":
            print("off")
        self.update()

    def __str__(self):
        return self.generateMessage()

if __name__ == '__main__':
    print(messageStat().generateMessage("test"))
