#This script file describes the client side functioning of a P2P system
#client.py

import socket

#setting up the socket connection
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host = socket.gethostname() // 154.46.20.237

#assigning the hostname of the RS server and the port 
host = "152.46.20.237"
port = 65423

s.connect((host,port))
print('Connection successful')
s.sendall("Hello, Server")

data = s.recv(1024)
s.close()

print("Received data from the server %s",repr(data))

