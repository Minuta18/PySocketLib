import socket

class ConnectedClient:
    def __init__(self, sock: socket.socket):
        self.conn, self.addr = sock.accept()
        self.conn.setblocking(False)

    def __del__(self):
        self.conn.close()