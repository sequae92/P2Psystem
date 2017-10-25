#To create a peer A

import server_peer as sp
import client
import socket

rs_hostname = '10.0.0.1'
rs_port = 65423
rfc_server_port = 60001

c = client.Client(rs_hostname,rs_port,rfc_server_port)
c.register()
c.pquery()
flag = False;
rfcsearch = "8266"
for i in c.active_peers:
    if i.hostname != socket.gethostname():
        c.rfcquery(i.hostname,i.rfc_server_port)
        for j in sp.Server_Peer.get_indexlist():
            if j.rfc_num == rfcsearch:
                print "Peer B has required RFC!!"
                flag = True
                hostname = j.peer_hostname

if flag:
    c.getrfc(rfcsearch,hostname)
