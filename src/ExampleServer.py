from PySocketLib.Server import TCPServer
from PySocketLib.Client import ConnectedClient
import socket

class MyServer(TCPServer):
    client_messages = dict()
    
    def connect_client(self, sock: socket.socket) -> ConnectedClient:
        new_client = super().connect_client(sock)
        print(f'[INFO] Connected client with address: {new_client.addr}')

    def disconnect_client(self, client: ConnectedClient):
        print(f'[INFO] Disconnect client with address: {client.addr}')
        return super().disconnect_client(client)

    def on_receive(self, data: bytes, client: ConnectedClient):
        self.client_messages[client] = data
        print(f'[INFO] Received {data}')
        return super().on_receive(data, client)
    
    def on_send(self, client: ConnectedClient):
        message = self.client_messages.get(client)
        if (message != None):
            print(f'[INFO] Sent data {message}')
            self.client_messages[client] = None
            return message
        else:
            return b''

if __name__ == '__main__':
    server = MyServer(('', 3000, 0, 0))
    
    while True:
        server.proceed()