opening_text0="""Checking all systems // Nominal

Connection // Waiting for upling // warning

Quality // Good // green
"""
connected="""Checking all systems // Nominal

Connection // Uplink established

Connection // Initiating handshake // warning

Quality // Good // green"""

handshake = """Checking all systems // Nominal

Connection // Uplink established

Connection // Handshake received

             Welcome {}

Quality // Good // green"""

handshake_error= """Checking all systems // Nominal

Connection // Uplink established

Connection // Handshake error // red

             Could not send through handshake, connection has been severed

Quality // Good // green"""

global_status = """ You are sucessfuly connected"""


connection_error="""Communication error // Connection refused // red

A communication could not be established with the server

Satus // Fatal // red"""

connection_terminated="""                     Connection terminated

The communication was severed from the central server

Status // Terminated // warning"""
