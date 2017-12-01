#To create a peer A

import server_peer as sp
import client
import socket
import time

rs_hostname = '10.0.0.1'
rs_port = 65423
rfc_server_port = 65401

c = client.Client(rs_hostname,rs_port,rfc_server_port)
c.register()
time.sleep(4)
c.pquery()
flag = False;
rfc_to_get = "8266"
for i in c.active_peers:
    if i.hostname != socket.gethostname():
        #print i.hostname,socket.gethostname()
        c.rfcquery(i.hostname,i.rfc_server_port)
        print "Completed RFC Query in peer A"
        indexlist = sp.Server_Peer.get_indexlist()
        print indexlist
        for j in indexlist:
            if j.rfc_num == rfc_to_get:
                print "{} has required RFC {}.".format(j.peer_hostname, rfc_to_get)
                flag = True
                hostname = j.peer_hostname
if flag:
    c.getrfc(rfc_to_get,hostname)
else:
    print "Indexlist obtained did not have information about the peer with the RFC number {}.".format(rfc_to_get)
time.sleep(5)
c.pquery()
for i in c.active_peers:
    print i.hostname
