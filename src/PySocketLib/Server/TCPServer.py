import socket
import selectors
import types

from PySocketLib.Server import Server
from PySocketLib.CExceptions.InitExceptions import UnablePort
from PySocketLib.Client import ConnectedClient

class TCPServer(Server):
    '''Simple TCP server'''
    def __init__(self, 
        host: str='0.0.0.0',
        port: int=8000,
    ):
        super().__init__(host, port)

    def connect_client(self, sock: socket.socket) -> ConnectedClient:
        return super().connect_client(sock)
    
    def disconnect_client(self, client: ConnectedClient):
        return super().disconnect_client(client)
    
    def on_receive(self, data: bytes, client: ConnectedClient):
        return super().on_receive(data, client)
    
    def on_send(self, client: ConnectedClient) -> bytes:
        return super().on_send(client)