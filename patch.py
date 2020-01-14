base="""!g+--------------------------------------------------------------------------------------
!g| {title}
!g+--------------------------------------------------------------------------------------
#g | Main deck // {self.deck}
#g| Comunication arrays // {self.comms}
#g| {self.main_events}
!g+-----------------------------
#g| Inertia compensator // {self.inertia}
#g| Vital systems // {self.survival}
#g| {self.vital_events}
!g+-----------------------------
#g| Reactor status // {self.reactor}
#g| Reactor power // {self.reactor_pw}
#g| {self.reactor_events}
!g+-----------------------------
#g| Propultion status // {self.propulsion}
#g| Lightfold engines // {self.lightfold}
#g| Propultion power // {self.propulsion_pw}
#g| {self.prop_events}
!g+-----------------------------
#g| Docks // {self.docks}
#g| Medical Bay // {self.medical}
#g| Quarters // {self.quarters}
#g| Baracks // {self.baracks}
#g| {self.misc_events}
!g+--------------------------------------------------------------------------------------

!g+-----------------------------
#g| Users connected {users}
!g+--------------------------------------------------------------------------------------
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
            ret+="Hull breach ! "
        if self.note[16]:
            ret+="Structural integrity critical ! "
        if self.note[18]:
            ret+="Foreign object alert !"

        if ret != "":
            ret="Critical Issue//"+ret+"//bred"
        return ret

    def update(self):
        self.deck=self.classical(self.cc[16])
        self.comms=self.classical(self.cc[17])

        self.inertia=self.classical(self.cc[20])
        self.survival=self.classical(self.cc[21])

        self.reactor=self.classical(self.cc[24])
        self.reactor_pw=self.powerlevel(self.cc[25])

        self.propulsion=self.classical(self.cc[28])
        self.lightfold=self.classical(self.cc[29])
        self.propulsion_pw=self.powerlevel(self.cc[30])

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
