#This script file describes the client side functioning of a P2P system

# This client must support 4 functions to the RS.
# Create a socket, shutdown and close a socket.
# Also, implement 2 peer functions.
# Maintain a peerlist and an indexlist as class variables that the server can access.
# Cookie goes into a file.

import sys
import socket

class Client:
    indexlist = []
    def __init__(self, rs_hostname, rs_port, rfc_server_port):
        self.hostname = socket.gethostname()
        self.rs_port = rs_port
        self.rs_hostname = rs_hostname
        self.rfc_server_port = rfc_server_port
        self.active_peers = []
        if os.path.exists("cookie.txt"):
            with open("cookie.txt") as f:
                self.cookie = f.read().strip()
        else:
            self.cookie = 0
            
    #start the socket connection
    def create_socket_and_connect(self, dest_hostname, dest_port):
	    try:
            sock = socket.socket(AF_INET, SOCK_STREAM)
        except socket.error, e:
            print "Socket could not be created"
            sys.exit(1) 
	    sock.connect((self.dest_hostname, dest_port))
	    return sock
    
    def send_msg(self, msg, sock):
        sock.sendall(msg)
        try:
            data = sock.recv(8192)
        except socket.error:
            print "Data receive failed."
            data = None
        return data

    def create_cookie_file(self):
        with open("cookie.txt", "w") as fileptr:
            fileptr.write(self.cookie)

    def register(self):
        '''
            Message format: "Register<sp>hostname<sp>cookie<sp>rfc_server_port"
        '''
        sock = self.create_socket_and_connect(self.rs_hostname, self.rs_port)
        msg = "Register " + self.hostname + " " + self.cookie + " " + self.rfc_server_port
        recv_data = self.send_msg(msg, sock) # Format: Register-OK<sp>cookie
        if recv_data:
            self.cookie = recv_data.split()[1]
            #print("Register Message sent to the RS Server")
            self.create_cookie_file()

        
    def pquery(self):
	    '''
                Message format: "PQuery<sp>cookie"
	    '''
        sock = self.create_socket_and_connect(self.rs_hostname, self.rs_port)
		msg = "PQuery " + self.cookie
		recv_data = self.send_msg(msg, sock)
		#print("PQuery message sent to the RS Server")
        if recv_data:
            if recv_data.split('\n')[0].endswith("Fail"):
                print "PQuery response from RS: Fail"
            else:
                # The Registration Server has sent a list of active peers, add them to peerlist.
                for line in recv_data.split('\n')[1:]:  # First line will have the line PQuery-OK
                    peer = Peer(line.split()[0], line.split()[1]) # Hostname and RFC Server port
                    self.active_peers.append(peer)
        else:
            print "PQuery: Receiver did not send any data back." 

    def keepalive(self):
        '''
                Message format: "Keepalive<sp>cookie"
        '''
        sock = self.create_socket_and_connect(self.rs_hostname, self.rs_port)
        msg = "Keepalive " + str(self.cookie)
		recv_data = self.send_msg(msg, sock)
        if recv_data 
            if recv_data.endswith("OK"):
                print "Keepalive successfully processed by the RS."
            else:
                print "Keepalive response from RS: Fail".
        else:
            print "PQuery: Receiver did not send any data back." 

    def leave(self):
        '''
                Message format: "Leave<sp>cookie"
        '''
        sock = self.create_socket_and_connect(self.rs_hostname, self.rs_port)
        msg = "Leave " + self.cookie
		recv_data = self.send_msg(msg, sock)
        if recv_data:
            if recv_data.endswith("OK"):
                print "Leave successfully processed by the RS."
            else:
                print "Leave response from RS: Fail."
        else:
            print "Leave: Receiver did not send any data back."

class Peer:
    def __init__(self, hostname, rfc_server_port):
        self.hostname = hostname
        self.rfc_server_port = port

def main():
    rs_port = 65423
    hostname = '152.46.20.81'
    cookie = 1
    rfc_server_port = 65750
 
    c = Client(rs_port,hostname,cookie,rfc_server_port) # instantiate with server port and hostname
    #rfc_peer = Server_Peer(port,hostname) # importing Server_Peer class

    #c.start_conn()
    #c.create_RFC_Server()
    c.client_register()
    #c.send_receive()
    #c.client_pquery()
    #c.client_keepalive()
    #c.client_leave()


if __name__ == '__main__':
    main()
