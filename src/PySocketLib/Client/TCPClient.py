from . import Client
from PySocketLib.Utility.Protocol import Protocol
from PySocketLib.CExceptions.RunTime import ServiceUnavailableException
from PySocketLib.Server.TCPServer import Message
import socket

class TCPClient(Client):
    def __init__(self,
        addr: tuple,       
        package_size: int=1024,
        use_ipv6: bool=False,      
    ):
        self._socket = None
        self._use_ipv6 = use_ipv6
        self.package_size = package_size
        if use_ipv6:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self._addr = addr
        self._socket.connect(addr)
        self.messages = list()
        # self._socket.setblocking(False)

    def __del__(self):
        self._socket.close()

    def _service_connection(self):
        recv_data = self._socket.recv(self.package_size)
        edit_data = self.on_receive(recv_data)
        self.messages.append(Message(
            self._socket.getsockname(),
            self._addr,
            edit_data,
            self.get_date(),
        ))

    def on_send(self, data: bytes):
        '''Actions to do when sending data'''
        return data

    def on_receive(self, data: bytes):
        '''Actions to do when receiving data'''
        return data

    def send(self, data: bytes):
        edit_data = self.on_send(data)
        self._socket.sendall(edit_data)
        self.messages.append(Message(
            self._addr,
            self._socket.getsockname(),
            edit_data,
            self.get_date(),
        ))
    
    def proceed(self):
        try:
            self._service_connection()
        except BlockingIOError as exception:
            raise ServiceUnavailableException("Can't connect to server")
        except BrokenPipeError as exception:
            raise ServiceUnavailableException("Can't connect to server")