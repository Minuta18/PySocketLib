import selectors
import socket

from PySocketLib.CExceptions.InitExceptions import UnablePort
from PySocketLib.Client import ConnectedClient

class Server:
    '''Simple socket server'''
    def __init__(self, 
        addr: tuple,
    ):
        self.__socket_selector = selectors.DefaultSelector()
        
        self.__socket = None
        if len(addr) == 2:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif len(addr) == 4:
            self.__socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        else:
            raise ValueError(f"Invalid address: {addr}")
        
        self.__socket.bind(addr)
        self.__socket.listen()
        self.__socket.setblocking(False)
        self.__socket_selector.register(self.__socket, selectors.EVENT_READ)
        self.__clients = dict()

    def __del__(self):
        '''Disconnects all clients'''
        self.__socket_selector.close()

    def __service_connection(self, key, mask):
        '''Proceed connection with client'''
        conn = key.fileobj

        if mask & selectors.EVENT_READ:
            recv_data = conn.recv(1024)
            if not recv_data:
                self.disconnect_client(self.__clients[conn])
            else:
                recv_data = self.on_receive(recv_data, self.__clients[conn])
        if mask & selectors.EVENT_WRITE:
            try:
                conn.sendall(self.on_send(self.__clients[conn]))
            except:
                pass

    def __connect_socket(self, sock: socket.socket) -> ConnectedClient:
        '''Connect socket'''
        new_client = ConnectedClient(sock)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.__socket_selector.register(new_client.conn, events, data='')
        self.__clients[new_client.conn] = new_client

        return new_client
    
    def connect_client(self, sock: socket.socket) -> ConnectedClient:
        '''Connect client'''
        return self.__connect_socket(sock)
    
    def disconnect_client(self, client: ConnectedClient):
        '''Disconnect client'''
        self.__socket_selector.unregister(client.conn)
        del self.__clients[client.conn]

    def on_receive(self, data: bytes, client: ConnectedClient) -> bytes:
        '''Actions to do when receiving data'''
        return data
    
    def on_send(self, client: ConnectedClient) -> bytes:
        '''Actions to do when sending data'''
        return b''
    
    def get_client(self, conn: socket.socket) -> ConnectedClient:
        '''Gets client by connection'''
        return self.__clients.get(conn)
        
    def get_client_by_addr(self, addr: str) -> ConnectedClient:
        '''Gets client by ip address'''
        for client in self.__clients.values():
            if client.addr == addr:
                return client
        return None
    
    def proceed(self):
        events = self.__socket_selector.select()
        for key, mask in events:
            if key.data == None:
                self.connect_client(key.fileobj)
            else:
                self.__service_connection(key, mask)