#This script file describes the client side functioning of a P2P system

# This client must support 4 functions to the RS.
# Create a socket, shutdown and close a socket.
# Also, implement 2 peer functions.
# Maintain a peerlist and an indexlist as class variables that the server can access.
# Cookie goes into a file.

import os
import sys
from socket import *
from threading import Timer
import server_peer

class Client:
    def __init__(self, rs_hostname, rs_port, rfc_server_port):
        self.hostname = gethostname()
        self.rs_port = rs_port
        self.rs_hostname = rs_hostname
        self.rfc_server_port = rfc_server_port
        self.active_peers = []
        if os.path.exists("cookie.txt"):
            with open("cookie.txt") as f:
                self.cookie = f.read().strip()
        else:
            self.cookie = 0

    def create_socket_and_connect(self, dest_hostname, dest_port):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
        except error:
            print "Socket could not be created"
            sys.exit(1) 
        sock.connect((dest_hostname, dest_port))
        return sock
    
    def send_msg_and_receive(self, msg, sock):
        sock.sendall(msg)
        try:
            data = sock.recv(8192)
        except error:
            print "Data receive failed."
            data = None
        return data

    def create_cookie_file(self):
        if not os.path.exists("cookie.txt"):
            with open("cookie.txt", "w") as fileptr:
                fileptr.write(self.cookie)

    def register(self):
        '''
            Message format: "Register<sp>hostname<sp>cookie<sp>rfc_server_port"
        '''
        sock = self.create_socket_and_connect(self.rs_hostname, self.rs_port)
        msg = "Register " + str(self.hostname) + " " + str(self.cookie) + " " + str(self.rfc_server_port)
        recv_data = self.send_msg_and_receive(msg, sock) # Format: Register-OK<sp>cookie
        if recv_data:
            if recv_data.split()[0].endswith("OK"):
                self.cookie = recv_data.split()[1]
                print "Register Successful!."
                self.create_cookie_file()
            else:
                print "Register response from RS: Fail."
        else:
            print "Register: Receiver did not send any data back."

        
    def pquery(self):
        '''
                Message format: "PQuery<sp>cookie"
        '''
        sock = self.create_socket_and_connect(self.rs_hostname, self.rs_port)
        msg = "PQuery " + str(self.cookie)
        #print "Message Done",msg
        recv_data = self.send_msg_and_receive(msg, sock)
        print("PQuery message sent to the RS Server")
        if recv_data:
            if recv_data.split('\n')[0].endswith("Fail"):
                print "PQuery response from RS: Fail"
            else:
                print("PQuery Successful!")        
                # The Registration Server has sent a list of active peers, add them to peerlist.
                if len(recv_data.split('\n')) > 1:
                    for line in recv_data.split('\n')[1:]:  # First line will have the line PQuery-OK
                        peer = Peer(line.split()[0],int(line.split()[1])) # Hostname and RFC Server port
                        self.active_peers.append(peer)
        else:
            print "PQuery: Receiver did not send any data back." 

    def keepalive(self):
        '''
                Message format: "Keepalive<sp>cookie"
        '''
        sock = self.create_socket_and_connect(self.rs_hostname, self.rs_port)
        msg = "Keepalive " + str(self.cookie)
        recv_data = self.send_msg_and_receive(msg, sock)
        if recv_data: 
            if recv_data.endswith("OK"):
                print "Keepalive successfully processed by the RS."
            else:
                print "Keepalive response from RS: Fail."
        else:
            print "Keepalive: Receiver did not send any data back." 

    def leave(self):
        '''
                Message format: "Leave<sp>cookie"
        '''
        sock = self.create_socket_and_connect(self.rs_hostname, self.rs_port)
        msg = "Leave " + str(self.cookie)
        recv_data = self.send_msg_and_receive(msg, sock)
        if recv_data:
            if recv_data.endswith("OK"):
                print "Leave successfully processed by the RS."
            else:
                print "Leave response from RS: Fail."
        else:
            print "Leave: Receiver did not send any data back."
            
    def rfcquery(self, peer_hostname, peer_rfc_server_port):
        sock = self.create_socket_and_connect(peer_hostname, peer_rfc_server_port)
        msg = "RFCQuery"
        recv_data = self.send_msg_and_receive(msg, sock)
        if recv_data:
            if recv_data.split('\n')[0].endswith("OK"):
                server_peer.Server_Peer.append_indexlist(recv_data.split('\n')[1:])
            else:
                print "RFCQuery response from peer with hostname {}: Fail.".format(peer_hostname)
        else:
            print "RFCQuery: Receiver with hostname {} did not send any data back.".format(peer_hostname)
                   
    def getrfc(self, rfc_num, peer_hostname):
        msg = "GetRFC {}".format(rfc_num)
        ret = self.send_rfc_req(msg, peer_hostname)
        if ret[0] == True:  # Ignore if not True.
            rfc_received = True
            with open("../rfc/{}.txt".format(rfc_num), "w") as f:
                print "Writing RFC data to rfc/{}.txt.".format(rfc_num)
                f.write(ret[1])
                server_peer.Server_Peer.build_local_indexlist()
                return True
        else:
            print "Get RFC {}: Fail.".format(rfc_num)
            return False

    def get_port_from_hostname(self, peer_hostname):
        for peer in self.active_peers:
            if peer.hostname == peer_hostname:
                return peer.rfc_server_port
        return None
        
    def send_rfc_req(self, msg, peer_hostname):
        # Find the port number of the peer with peer_hostname from peerlist.
        # Send a req to the peer, get the response. If Fail, return false. If OK, return true and the data. 
        peer_port = self.get_port_from_hostname(peer_hostname)
        if peer_port == None:
            print "Port for hostname {} not found.".format(peer_hostname)
        sock = self.create_socket_and_connect(peer_hostname, peer_port)
        recv_data = self.send_msg_and_receive(msg, sock)
        if recv_data:
            if recv_data.split('\n')[0].endswith("OK"):
                # First line indicates the status, which is OK. Data is second line onwards.
                return [True, '\n'.join(recv_data.split('\n')[1:])]
            else:
                # Status is fail.
                print "RFC Response from peer with hostname {}: Fail.".format(peer_hostname)
                return [False, None]
        else:
            print "RFC Response: Receiver with hostname {} did not send back any data.".format(peer_hostname)
            return [False, None]
        print "Peer with hostname {} does not exist in the peerlist.".format(peer_hostname)
        return [False, None]
                

class Peer:
    def __init__(self, hostname, rfc_server_port):
        self.hostname = hostname
        self.rfc_server_port = rfc_server_port


def main():
    rs_port = 65423
    hostname = '152.46.17.147'
    cookie = 1
    rfc_server_port = 65750
 
    c = Client(hostname, rs_port, rfc_server_port) # instantiate with server port and hostname
    #rfc_peer = Server_Peer(port,hostname) # importing Server_Peer class

    #c.start_conn()
    #c.create_RFC_Server()
    c.register()
    #c.send_receive()
    #c.client_pquery()
    #c.client_keepalive()
    #c.client_leave()


if __name__ == '__main__':
    main()
