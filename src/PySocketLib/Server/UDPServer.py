import socket
import os

from PySocketLib.Server import Server
from PySocketLib.Server.Server import Message
from PySocketLib.CExceptions.InitExceptions import UnablePort
from PySocketLib.CExceptions.RunTime import NoSuchClient
from PySocketLib.Client import ConnectedClient, ConnectedTCPClient, ConnectedUDPClient
from PySocketLib.Utility.Protocol import Protocol

class UDPServer(Server):
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
        self._clients = dict()
        self._messages = list()

    def __del__(self):
        pass

    def _server_socket_setup(self, addr: tuple) -> socket.socket:
        sock = None
        if len(addr) == 2:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif len(addr) == 4:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, 0)
        else:
            raise ValueError(f'Invalid address: {addr}')
        sock.bind(addr)

        return sock

    def _service_connection(self):
        data, addr = self._server_socket.recvfrom(self.package_size)
        if data != '' and data != None:
            new_msg = Message(addr, self._addr, self.on_receive(data), self.get_date())
            if self._clients.get(addr) == None:
                self._connect_client(addr)
            self._messages.append(new_msg)
        
    def _connect_client(self, addr) -> ConnectedUDPClient:
        new_client = ConnectedUDPClient(addr)
        self.on_connect(new_client)
        self._clients[addr] = new_client

        return new_client
    
    def _disconnect_client(self, client: ConnectedUDPClient):
        if self._clients.get(client.addr) == None:
            raise NoSuchClient(f'No such client: {client.addr}')
        self.on_disconnect(client.addr)
        del self._clients[client.addr]

    def send(self, data: bytes, client: ConnectedUDPClient):
        edited_data = self.on_send(data)
        new_message = Message(
            self._addr,
            client.addr,
            edited_data,
            self.get_date(),
        )
        self._messages.append(new_message)
        self._server_socket.sendto(edited_data, client.addr)

    def proceed(self):
        self._service_connection()