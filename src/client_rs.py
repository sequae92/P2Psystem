#This script file describes the client side functioning of a P2P system
#client.py

import sys
from datetime import *
import socket

class Client:
    #initialize all instance variables
    def __init__(self,port,hostname,cookie,rfc_server_port):
        self.port = port # this is rs server port
        self.hostname = hostname # this is in rs server hostname
        self.cookie = cookie
        self.rfc_server_port = rfc_server_port
        self.flag1 = 0
        self.flag2 = 0   	
            
    #start the socket connection
    def start_conn(self):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            hostname = ''
            print("Hostname and port ",self.hostname," Port: ",self.port)
            s.connect((self.hostname,self.port))
            print("Connection to RS is successful")

    #send and receive data after connection is setup
    def send_receive(self,conn):
        #s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#conn.connect((self.hostname,self.port))
	#s.sendall("Hello,Server")
        data = conn.recv(1024)
        print("Received data from the RS: ",str((data.split())[1]))

    def create_RFC_server(self):
        HOST = ''
        RFC_SERVER_PORT = 65450 # hardcoded for all RFC_Server ports on all peers, will keep another standby port
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #Bind socket to host port

        try:
            s.bind((HOST,RFC_SERVER_PORT))
        except socket.error as msg:
            print('Bind failed. Error code:' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
        print('Socket Bind complete')

        s.listen(10)
        #Now keep waiting for connection from the client
        while 1:
            conn,addr = s.accept()
            print('Connected with ' + addr[0] + ':' + str(addr[1]))
        s.close()

    def client_register(self):
        '''
                Message format: "Register<sp>hostname<sp>cookie<sp>rfc_server_port"
            '''
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #hostname = socket.gethostname()
        s.connect((self.hostname,self.port))

        msg = "Register abcde " + str(self.cookie) + " " + str(self.rfc_server_port)
        s.sendall(msg)
        print("Register Message sent to the RS Server")
	self.send_receive(s)

    def client_pquery(self):
	'''
                Message format: "PQuery<sp>hostname<sp>cookie"
	'''
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #hostname = socket.gethostname()
        s.connect((self.hostname,self.port))
        msg = "PQuery "+str(self.hostname)+" " + str(self.cookie)
        s.sendall(msg)
        print("PQuery message sent to the RS Server")


    def client_keepalive(self):
        '''
                Message format: "Keepalive<sp>hostname<sp>cookie"
            '''
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #hostname = socket.gethostname()
        s.connect((self.hostname,self.port))
        msg = "Keepalive "+str(self.hostname)+" " + str(self.cookie)
        s.sendall(msg)
        print("KeepAlive message sent to the RS Server")


    def client_leave(self):
        '''
                Message format: "Leave<sp>hostname<sp>cookie<sp>rfc_server_port"
            '''
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #hostname = socket.gethostname()
        s.connect((self.hostname,self.port))
        msg = "Leave "+str(self.hostname)+" " + str(self.cookie) + " " + str(self.rfc_server_port)
        s.sendall(msg)
        print("Leave message sent to the RS Server")


def main():
    port = 65423
    hostname = '152.46.20.81'
    cookie = 1
    rfc_server_port = 65750
 
    c = Client(port,hostname,cookie,rfc_server_port) # instantiate with server port and hostname
    #rfc_peer = Server_Peer(port,hostname) # importing Server_Peer class

    #c.start_conn()
    #c.create_RFC_Server()
    c.client_register()
    #c.send_receive()
    #c.client_pquery()
    #c.client_keepalive()
    #c.client_leave()


if __name__ == '__main__':
    main();
