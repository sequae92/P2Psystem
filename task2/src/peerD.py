import server_peer as sp
import client
import socket
import time

rs_hostname = '10.0.0.1'
rs_port = 65423
rfc_server_port = 65404
c = client.Client(rs_hostname,rs_port,rfc_server_port)
c.register()
time.sleep(8)
c.pquery()
downloaded_rfcs = set()    # A set.
# PQuery will return a list of Active peers and store it in c.active_peers.
# Get all index lists, merge.
# Then start a loop and look through the index list to get unique rfcs.

# For the best case, we DO NOT do rfcquery to all peers. We instead do rfcquery and getrfc in parallel, checking with our downloaded_rfcs set.
# If we have all RFCs (60 of them), we break.

for i in c.active_peers:
    # First get the Index from all.
    # Download the actual files and keep updating downloaded_rfcs.
    c.rfcquery(i.hostname, i.rfc_server_port)

indexlist = sp.Server_Peer.get_indexlist()
prev = 0
for index in indexlist:
    if index.rfc_num not in downloaded_rfcs:
        init_time = time.time()
        c.getrfc(index.rfc_num, index.peer_hostname)
        final_time = time.time()
        cur_time = final_time - init_time + prev
        prev = cur_time
        downloaded_rfcs.add(index.rfc_num)
        print "CUR TIME:", cur_time, index.rfc_num

