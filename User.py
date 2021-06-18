import socket
import Config
import threading
class User:
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
        self.is_closed = False

    def __enter__(self):
        self.socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM
            )
        self.socket.connect(self.address)
        return self

    def __exit__(self, *args):
        print(args)
        self.socket.close()

    def client_handler(self):
        conn = self.socket
        t = threading.Thread(target=self.send_msg, args=(conn,))
        t.start()
        while not self.is_closed:
            msg = conn.recv(self.msg_length)
            msg = msg.decode(self.encoding)
            if msg:
                print(msg)
                if msg==self.disconnect_msg:
                    self.is_closed = not self.is_closed
        
    def send_msg(self, conn):
        last_msg = ''
        while last_msg != self.disconnect_msg:
            inp = input()
            last_msg = inp
            conn.send(last_msg.encode(self.encoding))
            if self.is_closed:
                break

if __name__ == '__main__':
    host_name = socket.gethostbyname(socket.gethostname())
    with User(Config.PORT, Config.HOST_NAME) as server:
        server.client_handler()