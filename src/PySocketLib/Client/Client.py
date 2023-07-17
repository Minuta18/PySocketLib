import socket
from PySocketLib.Utility.Protocol import Protocol
from abc import ABC, abstractmethod

class Client:
    '''Simple socket client'''
    def __init__(self, 
        addr: tuple,
    ):
        self._addr = addr

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
    
    def proceed(self):
        self._service_connection()