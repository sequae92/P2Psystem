from socket import *
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('152.46.20.237' , 65423))
sock.sendall('register this')
print sock.recv(4096)
