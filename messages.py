opening_text0="""##  Checking all systems // Nominal

## Connection // Waiting for upling // orange // bgreen

## Quality // Good // green
"""
connected="""## Checking all systems // Nominal

## Connection // Uplink established

## Connection // Initiating handshake // orange

## Quality // Good // bgreen"""

handshake = """## Checking all systems // Nominal

## Connection // Uplink established

## Connection // Handshake received

##                       Welcome {}

##Quality // Good // bgreen"""

handshake_error= """##Checking all systems // Nominal

##Connection // Uplink established

##Connection // Handshake error // red

!r             Could not initiate handshake, connection has been severed

## Satus // Fatal // bred

## Quality // Worst // bred"""

global_status = """## You are sucessfuly connected """


connection_error="""## Communication error // Connection refused // red

!r       A communication could not be established with the central network command
!o       Retrying connection, please wait for uplink or check network redondancies

## Satus // Fatal // bred
## Quality // Worst // bred"""

connection_terminated="""##                     Connection terminated

## The communication was severed from the central server

## Status // Terminated // borange"""

retrying_connection="""## Checking all systems // Warning //borange

## Connection // Retrying connection // orange // bgreen

## Quality // Bad // orange"""
