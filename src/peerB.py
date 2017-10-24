#To create a peer B

import server_peer as sp
import client

rs_hostname = '10.0.0.1'
rs_port = 65423
rfc_server_port = 60002

c = client.Client(rs_hostname,rs_port,rfc_server_port)
c.register()
'''
c.pquery()
flag = False;
rfcsearch = "8266"
for i in c.active_peers:
    c.rfcquery(i.hostname,i.rfc_server_port)
    for j in Client.indexlist:
        if j.rfc_num == rfcsearch:
            print "Peer B has required RFC!!"
            flag = True
            hostname = j.peer_hostname

if flag:
    c.getrfc(rfcsearch,hostname)
'''
