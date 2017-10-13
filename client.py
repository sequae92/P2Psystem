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

def client_register():
	

def client_pquery():

def client_keepalive():

def client_leave():
