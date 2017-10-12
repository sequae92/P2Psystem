import sys
import thread
from socket import *

class Server:
    def __init__(self, port):
        self.port = port
        self.hostname = ""
        self.sock = None
    
    def create_and_bind_socket(self):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
        except: # Change this line.
            print "Socket could not be created" # log instead.
            sys.exit(1)
        if self.sock is not None:
            try:
                self.sock.bind((self.hostname, self.port))
            except Exception as e:
                print e.message
                print "Could not bind socket to port! Exiting"
                self.shutdown_and_close()
                sys.exit(1)

    def shutdown_and_close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            print "Socket shutdown successfully."
        except Exception as e:
            print e.message, " Couldn't shutdown the socket on the server."
        try:
            self.sock.close()
        except Exception as e:
            print e.message, " Couldn't close the socket"

    def main_loop(self):
        while True:
            self.sock.listen(1)
            conn, cli_addr = self.sock.accept()
            print "Accepting conn with", cli_addr
            thread.start_new_thread(self.process_request, (conn,))
        
    def process_request(self, conn):
        msg = conn.recv(4096)
        if msg.split()[0] == "register":
            self.process_reg(msg, conn)
        elif msg.split()[0] == "leave":
            self.process_leave(msg, conn)
        elif msg.split()[0] == "pquery":
            self.process_pquery(msg, conn)
        elif msg.split()[0] == "keepalive":
            self.process_keepalive(msg, conn)

    def process_reg(self, msg, conn):
        '''
        Message format: "Register<sp>hostname<sp>cookie<sp>rfcserverport"
        '''
        # conn.send() of new/existing cookie value.
        self.update_records('''param?''')

    def process_leave(self, msg, conn):
        pass

    def process_pquery(self, msg, conn):
        pass
    
    def process_keepalive(self, msg, conn):
        pass
 

def main():
    PORT_NUM = 65423
    s = Server(PORT_NUM)
    s.create_and_bind_socket()
    s.main_loop()
if __name__ == '__main__':
    main() 

# Create main_loop which runs forever.
# Accept connections and create a thread to process the request.




