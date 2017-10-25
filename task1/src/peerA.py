#To create a peer A

import server_peer as sp
import client
import socket
import time

rs_hostname = '10.0.0.1'
rs_port = 65423
rfc_server_port = 60001

c = client.Client(rs_hostname,rs_port,rfc_server_port)
c.register()
time.sleep(4)
