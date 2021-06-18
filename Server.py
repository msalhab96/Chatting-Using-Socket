import Config
import socket
import threading
import os

class Peer2Peer:
    def __init__(
        self, 
        port, 
        host_name, 
        msg_length=1024,
        encoding='utf-8',
        disconnect_msg='-STOP-'
        ):
        self.port = port
        self.host_name = host_name
        self.address = (self.host_name, self.port)
        self.disconnect_msg = disconnect_msg
        self.encoding = encoding
        self.msg_length = msg_length
        self.socket = None

    def __enter__(self):
        self.socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM
            )
        self.socket.bind(self.address)
        self.socket.listen()
        return self

    def __exit__(self):
        self.socket.close()

    def accept_clients(self):
        while True:
            conn, addr = self.socket.accept()
            t1 = threading.Thread(target=self.client_handler, args=(conn, addr))
            t2 = threading.Thread(target=self.send_msg, args=(conn, addr))
            t1.start()
            t2.start()

    def client_handler(self, conn, addr):
        print(addr)
        is_closed = False
        while not is_closed:
            msg = conn.recv(self.msg_length)
            msg = msg.decode(self.encoding)
        
    def send_msg(self, conn, addr):
        last_msg = ''
        while last_msg != self.disconnect_msg:
            inp = input()
            last_msg = inp
            conn.sendto(last_msg.encode(self.encoding), addr)
        
if __name__ == '__main__':
    with Peer2Peer(Config.PORT, Config.HOST_NAME) as server:
        server.accept_clients()