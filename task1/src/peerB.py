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
time.sleep(8)
c.pquery()
flag = False;
# PQuery will return a list of Active peers and store it in c.active_peers.
# Find peerA from this list, request the index list
for i in c.active_peers:
    # Running peerA on server01.
    if i.hostname == "server01":
        c.rfcquery(i.hostname, i.rfc_server_port)
        print "RFC Query from PeerB to PeerA complete."
        # Now that we have the hostname and port of PeerA, execute getrfc for all RFCs.
        indexlist = sp.Server_Peer.get_indexlist()
        rfc_count = 0
        prev = 0
        for index in indexlist:
            # PeerA has all RFCs. Download them.
            if rfc_count < 50:
                init_time = time.time()
                c.getrfc(index.rfc_num, index.peer_hostname)
                final_time = time.time()
                cur_time = final_time - init_time + prev
                prev = cur_time
                print "CUR TIME:", cur_time, index.rfc_num
                print "GetRFC from PeerB to PeerA complete." 
            else:
                print "All 50 RFCs downloaded."
                break
            rfc_count += 1

