from . import Client
from PySocketLib.Utility.Protocol import Protocol
from PySocketLib.CExceptions.RunTime import ServiceUnavailableException
import socket

class TCPClient(Client):
    def __init__(self,
        addr: tuple,             
    ):
        self._socket = None
        if len(addr) == 2:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif len(addr) == 4:
            self._socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            raise ValueError(f"Invalid address: {addr}")
        self._socket.connect(addr)
        # self._socket.setblocking(False)

    def __del__(self):
        self._socket.close()

    def _service_connection(self):
        recv_data = self._socket.recv(1024)
        self.on_receive(recv_data)

    def on_send(self, data: bytes):
        '''Actions to do when sending data'''
        return data

    def on_receive(self, data: bytes):
        '''Actions to do when receiving data'''
        return data

    def send(self, data: bytes):
        self._socket.sendall(self.on_send(data))
    
    def proceed(self):
        try:
            self._service_connection()
        except BlockingIOError as exception:
            raise ServiceUnavailableException("Can't connect to server")
        except BrokenPipeError as exception:
            raise ServiceUnavailableException("Can't connect to server")