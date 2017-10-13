from socket import *
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('' , 65423))
hostname = gethostname()
sock.sendall("Register "+hostname+" 0 65500")
print sock.recv(4096)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('' , 65423))
hostname = gethostname()
sock.sendall("Register "+hostname+" 0 65500")
print sock.recv(4096)

time.sleep(3)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('' , 65423))
hostname = gethostname()
sock.sendall("Leave "+hostname+" 1 65500")
print sock.recv(4096)
