from PySocketLib.Utility.Protocol import Protocol
import socket

class ConnectedClient:
    addr: tuple
    conn: None

class ConnectedTCPClient(ConnectedClient):
    def __init__(self, sock: socket.socket):
        self.conn, self.addr = sock.accept()
        self.conn.setblocking(False)

    def __del__(self):
        self.conn.close()

class ConnectedUDPClient(ConnectedClient):
    def __init__(self, addr):
        self.addr = addr