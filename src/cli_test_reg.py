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

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('' , 65423))
hostname = gethostname()
sock.sendall("PQuery "+" 1")
print sock.recv(4096)

'''
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('' , 65423))
hostname = gethostname()
sock.sendall("Leave "+hostname+" 3 65500")
print sock.recv(4096)'''

time.sleep(36)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('' , 65423))
hostname = gethostname()
sock.sendall("Keepalive "+" 1")
print sock.recv(4096)

time.sleep(40)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('' , 65423))
hostname = gethostname()
sock.sendall("Keepalive "+" 2")
print sock.recv(4096)







