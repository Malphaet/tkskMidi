opening_text0="""#g Checking all systems // Nominal

#g Connection // Waiting for upling // orange

#g Quality // Good // green
"""
connected="""#g Checking all systems // Nominal

#g Connection // Uplink established

#g Connection // Initiating handshake // orange

#g Quality // Good // bgreen"""

handshake = """#g Checking all systems // Nominal

#g Connection // Uplink established

#g Connection // Handshake received

#g                       Welcome {}

#g Quality // Good // bgreen"""

handshake_error= """#g Checking all systems // Nominal

#g Connection // Uplink established

#g Connection // Handshake error // red

!r             Could not initiate handshake, connection has been severed

#g Satus // Fatal // bred

#g Quality // Worst // bred"""

global_status = """#g You are sucessfuly connected """


connection_error="""#g Communication error // Connection refused // red

!r       A communication could not be established with the central network command
!o       Retrying connection, please wait for uplink or check network redondancies



#G Try number // {tnumber} // borange

#g Satus // Fatal // bred
#g Quality // Worst // bred"""

connection_terminated="""#g                    Connection terminated

#g The communication was severed from the central server

#g Status // Terminated // borange"""

retrying_connection="""#g Checking all systems // Warning //borange

#g Connection // Retrying connection // orange

#g Quality // Bad // orange"""
