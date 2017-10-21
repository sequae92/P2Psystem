    #This script file describes the client side functioning of a P2P system
    #client.py

    import sys
    from datetime import *
    from socket import *
    from datetime import *

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
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        hostname = socket.gethostname()
        s.connect((hostname,port))
        print("Connection to RS is successful")

    #send and receive data after connection is setup
    def send_receive(self):
        s.sendall("Hello,Server")
        data = s.recv(1024)
        print("Received data from the RS",repr(data))

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

    def client_register(self,cookie):
        '''
                Message format: "Register<sp>hostname<sp>cookie<sp>rfc_server_port"
            '''
        rfc_server_port = 65450
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        hostname = socket.gethostname()
        s.connect((hostname,rfc_server_port))

        if()
        msg = "Register<sp>"+hostname+"<sp>" + cookie + "<sp>" + rfc_server_port
        s.sendall(msg)
        print("Register Message sent to the RS Server")

    def client_pquery():
            '''
                Message format: "PQuery<sp>hostname<sp>cookie<sp>rfc_server_port"
            '''
        rfc_server_port = 65450
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        hostname = socket.gethostname()
        s.connect((hostname,rfc_server_port))
        msg = "PQuery<sp>"+hostname+"<sp>" + cookie + "<sp>" + rfc_server_port
        s.sendall(msg)
        print("PQuery message sent to the RS Server")


    def client_keepalive():
        '''
                Message format: "Keepalive<sp>hostname<sp>cookie<sp>rfc_server_port"
            '''
        rfc_server_port = 65450
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        hostname = socket.gethostname()
        s.connect((hostname,rfc_server_port))
        msg = "Register<sp>"+hostname+"<sp>" + cookie + "<sp>" + rfc_server_port
        s.sendall(msg)
        print("KeepAlive message sent to the RS Server")


    def client_leave():
        '''
                Message format: "Leave<sp>hostname<sp>cookie<sp>rfc_server_port"
            '''
        rfc_server_port = 65450
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        hostname = socket.gethostname()
        s.connect((hostname,rfc_server_port))
        msg = "Leave<sp>"+hostname+"<sp>" + cookie + "<sp>" + rfc_server_port
        s.sendall(msg)
        print("Leave message sent to the RS Server")


    def main():
            port = 65470
            c = Client(port)
            c.start_conn()
            c.create_RFC_server()
            c.client_register()
            c.client_pquery()
            c.client_keepalive()
            c.client_leave()


    if '__init__' == '__main__':
        main();
