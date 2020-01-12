opening_text0="""Checking all systems // Nominal

Connection // Waiting for upling // orange

Quality // Good // green
"""
connected="""Checking all systems // Nominal

Connection // Uplink established

Connection // Initiating handshake // orange

Quality // Good // bgreen"""

handshake = """Checking all systems // Nominal

Connection // Uplink established

Connection // Handshake received

             Welcome {}

Quality // Good // bgreen"""

handshake_error= """Checking all systems // Nominal

Connection // Uplink established

Connection // Handshake error // red

!             Could not initiate handshake, connection has been severed

Quality // Good // bgreen"""

global_status = """ You are sucessfuly connected"""


connection_error="""Communication error // Connection refused // red

A communication could not be established with the server

Satus // Fatal // bred"""

connection_terminated="""                     Connection terminated

The communication was severed from the central server

Status // Terminated // borange"""
