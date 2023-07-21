import socket
from PySocketLib.Utility.Protocol import Protocol
from PySocketLib.Server.TCPServer import Message
from abc import ABC, abstractmethod

class Client:
    '''Simple socket client'''
    def __init__(self, 
        addr: tuple,
    ):
        self._addr = addr
        self.messages = list()

    def __del__(self):
        pass

    @abstractmethod
    def _service_connection(self):
        pass

    def on_send(self, data: bytes):
        '''Actions to do when sending data'''
        return data

    def on_receive(self, data: bytes):
        '''Actions to do when receiving data'''
        return data
    
    @abstractmethod
    def send(self, data: bytes):
        pass
    
    def get_messages(self) -> list[Message]:
        return self.messages
    
    def get_messages_from_server(self) -> list[Message]:
        return [msg for msg in self.messages if msg.from_ == self._addr]
    
    def get_messages_from_client(self) -> list[Message]: 
        return [msg for msg in self.messages if msg.from_ != self._addr]

    def proceed(self):
        self._service_connection()

    def get_date(self):
        return ''