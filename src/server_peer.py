import sys
import thread
import os
from threading import Timer
from socket import *
from datetime import *
import client

class Server_Peer:
    indexlist = []
    def __init__(self, port):
        self.port = port
        self.hostname = ""
        self.sock = None
        self.build_index_list()
    
    def build_index_list(self):
        rfcfiles = os.listdir("../rfc")
        # 8266.txt: Format of the RFC text files in the rfc directory.
        # Assuming only such files exist in the rfc directory.
        # Get only the RFC number, for each RFC file.
        map(lambda x:x[:-4], rfcfiles)

        for i in rfcfiles:
            rfc_title = self.get_rfc_title_by_num(i)
            this_hostname = gethostname()
            index = Index(i, rfc_title, this_hostname)
            # Create a timer object but don't start it.
            # This index is based on local RFCs so it should not be removed from indexlist.
            index.timer = Timer(72, self.update_index_timer, [i, this_hostname])
            Server_Peer.indexlist.append(index)

    def update_index_timer(self, rfc_num, rfc_hostname):
        index = find_index(rfc_num, rfc_hostname)
        if index == None:
            print "Index for hostname {0} and RFC number {1} does not exist.".format(rfc_hostname, rfc_num)
        else:
            # Check if it is a local index or an index shared by somebody else.
            # A local index will never have a timer that is running.
            if index.timer.is_alive():
                index.timer.cancel()
                Server_Peer.indexlist.remove(index)
                print "Timer expired for index with hostname {0} and RFC number {1}:".format(rfc_hostname, rfc_num)
            else:
                print "Error: Local index expired for hostname {0} and RFC number {1}".format(rfc_hostname, rfc_num)

    def find_index(self, rfc_num, rfc_hostname):
        for i in Server_Peer.indexlist:
            if i.rfc_num == rfc_num and i.rfc_hostname == rfc_hostname:
                return i
        return None
    
    def get_rfc_title_by_num(self, num):
        return "TITLE" # How do we implement this?  

    @staticmethod
    def append_index(self, recv_data):
        # Assuming the client sends valid data here and handles error conditions.
        for line in lines:
            # Each line is an index.
            rfc_num =line.split()[0]
            rfc_hostname = line.split()[1]
            rfc_title = line.split()[2:]    # Title may have spaces, put it at the end.
            if find_index(rfc_num, rfc_hostname) is None:
                # If this index doesn't exist, create an Index object and append to indexlist.
                index = Index(rfc_num, rfc_hostname, rfc_title)
                index.timer = Timer(72, self.update_index_timer, [rfc_num, rfc_hostname])
                # Start a timer as this is potentially information about a remotely present RFC.
                index.timer.start()
                # Merge the new entry with the local indexlist.
                Server_Peer.indexlist.append(index)
            # else: Refresh the timer if the same index has been received by somebody else?         
                        
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
    
    def process_request(self, conn):
        msg = conn.recv(4096)
        if msg == "RFCQuery":
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
        if Server_Peer.indexlist:
            for i in Server_Peer.indexlist:
                if i.timer.is_alive():
                    index_str = "{0}, {1}, {2}".format(i.rfc_num, i.peer_hostname, i.rfc_title)
                rfc_index_l.append(index_str)
        else:
            pass #add a message
        to_send = "RFC-Index-OK\n" + '\n'.join(rfc_index_l)
        conn.send(to_send)           

    def process_get_rfc(self, msg, conn):
        '''
            Message format: "GetRFC<sp>RFCNumber"
        '''
        # Search for the RFC in the rfc directory and read the file and send it.
        rfc_num = msg.split()[1]
        fname = "../rfc/{}.txt".format(rfc_num)
        if os.path.exists(fname):
            with open(fname) as f:
                to_send = "GetRFC-OK\n"
                to_send += f.read()
                conn.send(to_send)
        else:
            conn.send("GetRFC-Fail")
    

class Index:
    def __init__(self, rfc_num, rfc_title, peer_hostname):
        self.rfc_num = rfc_num
        self.rfc_title = rfc_title
        self.peer_hostname = peer_hostname
        self.timer = None
   
 
def main():
    port = 60002 # Add a port of the peer
    s = Server_Peer(port)
    s.create_and_bind_socket()
    s.main_loop()

if __name__ == '__main__':
    main()
