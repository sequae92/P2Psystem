#This script file describes the client side functioning of a P2P system
#client.py

import sys
from datetime import *
import socket

class Client:

#initialize all instance variables
def __init__(self,port,hostname,cookie,flag1,flag2):
	self.port = port
	self.hostname = hostname
	self.cookie = cookie
	self.flag1 = flag1
	self.flag2 = flag2

#start the socket connection
def start_conn():
	s= socket.socket.AF_INET,socket.SOCK_STREAM)
        hostname = socket.gethostname()
	s.connect((hostname,port))
	print("Connection to RS is successful")

#send and receive data after connection is setup
def send_receive():
	s.sendall("Hello,Server")
	data = s.recv(1024)
	print("Received data from the RS",repr(data))

def create_RFC_server():
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
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
	s.close()
	
def client_register():
        '''
            Message format: "Register<sp>hostname<sp>cookie<sp>rfc_server_port"
        '''
	rfc_server_port = 65450
	msg = "Register<sp>"+hostname+"<sp>" + cookie + "<sp>" + rfc_server_port
	s.sendall(msg)
	print("Message sent to the RS Server")

def client_pquery():

def client_keepalive():

def client_leave():

def main():
		


if '__init__' == '__main__':
	main();
