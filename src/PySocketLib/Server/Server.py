import selectors
import socket

from PySocketLib.CExceptions.ProtocolExceptions import InvalidAddr
from PySocketLib.Client import ConnectedClient, ConnectedTCPClient
from PySocketLib.Utility.Protocol import Protocol
import datetime

from abc import ABC, abstractmethod

class Message():
    from_: tuple
    to: tuple
    content: str
    date = None

    def __init__(self, 
        from_: tuple, 
        to_: tuple, 
        content: str,
        date,
    ):
        self.from_ = from_
        self.to = to_
        self.content = content
        self.date = date

    def __str__(self):
        return f'[{self.date}] received from {self.from_} to {self.to}: {self.content}'
    
    def __repr__(self):
        return f'[{self.date}] received from {self.from_} to {self.to}: {self.content}'

class Server(ABC):
    '''Socket server abstract class'''
    def __init__(self,
        addr: tuple,             
        package_size: int=1024,
    ):
        try:
            self._ip_addr, self._port = addr
            self._addr = addr
            self.package_size = package_size
        except ValueError as e:
            raise ValueError('Invalid address')
        self._server_socket = self._server_socket_setup(addr)
        self._socket_selector = self._selector_setup(self._server_socket)
        self._clients = dict()
        self._messages = list()

    @abstractmethod
    def __del__(self):
        '''Close all connections'''
        pass

    @abstractmethod
    def _server_socket_setup(self, addr: tuple) -> socket.socket:
        '''Setup server socket'''
        pass

    def _selector_setup(self, server_socket: socket.socket):
        '''Setup selector'''

        socket_selector = selectors.DefaultSelector()
        socket_selector.register(server_socket, selectors.EVENT_READ)
        
        return socket_selector

    @abstractmethod
    def _service_connection(self, key, mask):
        '''Service connection'''
        raise NotImplementedError

    @abstractmethod
    def _connect_client(self, sock: socket.socket) -> ConnectedClient:
        '''Connects client to server'''
        raise NotImplementedError

    @abstractmethod
    def _disconnect_client(self, sock: socket.socket):
        '''Disconnects client from server'''
        raise NotImplementedError

    def get_addr(self) -> tuple:
        '''Returns address and port'''
        return self._addr

    def clear_messages(self):
        '''Remove all messages'''
        del self._messages[:]

    def get_messages(self) -> list[Message]:
        '''Returns all messages'''
        return self._messages
    
    def get_messages_from_clients(self) -> list[Message]:
        '''Returns all messages sent to server'''
        return [msg for msg in self._messages if msg.to == self.get_addr()]
    
    def get_messages_from_server(self) -> list[Message]:
        '''Returns all messages sent to clients'''
        return [msg for msg in self._messages if msg.from_ == self.get_addr()]
    
    def get_client_by_addr(self, addr):
        '''Returns a client with given address'''
        for client in self._clients.values():
            if client.addr == addr:
                return client
    
    @abstractmethod
    def send(self, data: bytes, client: ConnectedClient) -> Message:
        '''Sends a message to a client'''
        raise NotImplementedError

    def on_disconnect(self, client: ConnectedClient):
        '''Actions to do when disconnect client'''
        return client

    def on_connect(self, client: ConnectedClient):
        '''Actions to do when connect client'''
        return client

    def on_receive(self, data: bytes) -> bytes:
        '''Actions to do when receiving data'''
        return data

    def on_send(self, data: bytes) -> bytes:
        '''Actions to do when receiving data'''
        return data
    
    def get_date(self):
        '''Get current date'''
        return datetime.datetime.now().strftime('%H:%M:%S')

    @abstractmethod
    def proceed(self):
        '''Proceed all'''
        raise NotImplementedError