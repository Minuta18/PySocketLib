from PySocketLib.Server import TCPServer
from PySocketLib.Client import ConnectedClient, ConnectedTCPClient
import socket
import datetime

class MyServer(TCPServer):
    def get_date(self):
        return str(datetime.datetime.now())
    
    def on_connect(self, client: ConnectedClient):
        print(f'Connected client {client.addr}')
        return client
    
    def on_disconnect(self, client: ConnectedClient):
        print(f'Disconnected client {client.addr}')
        return client
    
    def on_send(self, data: bytes):
        print(f'Sent data: {data}')
        return data

    def on_receive(self, data: bytes):
        print(f'Received data: {data}')
        return data

if __name__ == '__main__':
    server = MyServer(('127.0.0.1', 3000))
    
    while True:
        server.proceed()

        for msg in server.get_messages_from_clients():
            server.send(msg.content, server.get_client_by_addr(msg.from_))

        server.clear_messages()