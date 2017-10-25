#To create a peer B

import server_peer as sp
import client
import socket
import time

rs_hostname = '10.0.0.1'
rs_port = 65423
rfc_server_port = 65402
c = client.Client(rs_hostname,rs_port,rfc_server_port)
c.register()
time.sleep(4)
c.pquery()
flag = False;
rfcsearch = "8205"
for i in c.active_peers:
    if i.hostname != socket.gethostname():
        print i.hostname,socket.gethostname()
        c.rfcquery(i.hostname,i.rfc_server_port)
        print "Completed RFC Query in peer B"
        indexlist = sp.Server_Peer.get_indexlist()
        print indexlist
        for j in indexlist:
            if j.rfc_num == rfcsearch:
                print "{} has required RFC {}.".format(j.peer_hostname, rfcsearch)
                flag = True
                hostname = j.peer_hostname
if flag:
    c.getrfc(rfcsearch,hostname)
else:
    print "Indexlist obtained did not have information about the peer with the RFC number {}.".format(rfc_to_get)
c.leave()
