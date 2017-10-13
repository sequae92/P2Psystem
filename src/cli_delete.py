from socket import *
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('' , 65423))
hostname = gethostname()
sock.sendall("Register "+hostname+" 2 65500")
print sock.recv(4096)
