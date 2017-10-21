import sys
import thread
from threading import Timer
from socket import *
from datetime import *
import client_peer

class Server_Peer:
    def __init__(self, port):
        self.port = port
        self.hostname = ""
        self.sock = None
    
    def create_and_bind_socket(self):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
        except:
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
            print e.message, "Couldn't shutdown the socket on the server."
        try:
            self.sock.close()
        except Exception as e:
            print e.message, "Couldn't close the socket"
    
    def process_request(conn):
        msg = conn.recv(4096)
        if msg.split()[0] == "RFCQuery":
            self.process_rfc_query(msg, conn)
        elif msg.split()[0] == "GetRFC":
            self.process_get_rfc(msg, conn)                

    def main_loop(self):
        while True:
            self.sock.listen(1)
            conn, cli_addr = self.sock.accept()
            print "Accepting conn with", cli_addr
            thread.start_new_thread(self.process_request, (conn,)) 

    def process_rfc_query(self, msg, conn):
        '''
            Message format: "RFCQuery"
        '''
        # Look through the indexlist maintained by the client and send the currently active entries.
        # Extract information from the Index objects and add to a string and send back.
        rfc_index_l = []
        if client_peer.indexlist:
            for i in client_peer.indexlist:
                if i.timer.is_alive():
                    # time.time() rounded off to the nearest second and converted to an int.
                    time_left = int(round(time.time())) - i.ttl
                index_str = "{}, {}, {}, {}".format(i.rfc_num, i.rfc_title, i.peer_hostname, time_left)
                rfc_index_l.append(index_str)
        to_send = "RFC-Index\n" + '\n'.join(rfc_index_l)
        conn.send(to_send)           

    def process_get_rfc(self, msg, conn):
        '''
            Message format: "GetRFC<sp>RFCNumber"
        '''
        # Search for the RFC in the rfc directory and read the file and send it.
        rfc_num = msg.split()[1]
        fname = "../{}".format(rfc_num)
        if os.path.exists(fname):
            with open(fname) as f:
                to_send = "RFC {}\n".format(rfc_num)
                to_send += f.read()
                conn.send(to_send)
        else:
            conn.send("GetRFC-Fail")
        
def main():
    port = 64423
    s = Server(port)
    s.create_and_bind_socket()
    s.main_loop()

if __name__ == '__main__':
    main()
