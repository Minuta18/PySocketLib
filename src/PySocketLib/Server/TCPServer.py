import socket
import selectors
import types

from PySocketLib.Server.Server import Server
from PySocketLib.Server.Server import Message
from PySocketLib.CExceptions.InitExceptions import UnablePort
from PySocketLib.Client import ConnectedTCPClient, ConnectedClient

class TCPServer(Server):
    '''Simple TCP server'''
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

    def __del__(self):
        self._socket_selector.close()

    def _selector_setup(self, server_socket: socket.socket):
        '''Setup selector'''
        socket_selector = selectors.DefaultSelector()
        socket_selector.register(server_socket, selectors.EVENT_READ)

        return socket_selector

    def _service_connection(self, key, mask):
        '''Service connection'''
        conn = key.fileobj

        if mask & selectors.EVENT_READ:
            try:
                recv_data = conn.recv(self.package_size)
            except ConnectionResetError:
                self._disconnect_client(self._clients[conn])
                return
            if not recv_data:
                self._disconnect_client(self._clients[conn])
            else:
                recv_data = self.on_receive(recv_data)
                self._messages.append(Message(
                    self._clients[conn].addr,
                    self._addr,
                    recv_data,
                    self.get_date(),
                ))

    def _server_socket_setup(self, addr: tuple) -> socket.socket:
        sock = None
        if len(addr) == 2:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif len(addr) == 4:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        else:
            raise ValueError(f'Invalid address: {addr}')
        
        sock.bind(addr)
        sock.listen()
        sock.setblocking(False)

        return sock
    
    def _connect_client(self, sock: socket.socket) -> ConnectedClient:
        new_client = ConnectedTCPClient(sock)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self._socket_selector.register(new_client.conn, events, data='')
        self._clients[new_client.conn] = new_client

        return new_client
    
    def _disconnect_client(self, client: ConnectedTCPClient):
        self.on_disconnect(client)
        self._socket_selector.unregister(client.conn)
        
        del self._clients[client.conn]
    
    def send(self, data: bytes, client: ConnectedTCPClient) -> Message:
        new_message = Message(
            self._addr,
            client.addr,
            data,
            self.get_date(),
        )
        self._messages.append(new_message)
        client.conn.sendall(self.on_send(data))
        return new_message

    def proceed(self):
        events = self._socket_selector.select(timeout=5)
        for key, mask in events:
            if key.data == None:
                new_client = self._connect_client(key.fileobj)
                self.on_connect(new_client)
            else:
                self._service_connection(key, mask)