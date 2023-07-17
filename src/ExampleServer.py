from PySocketLib.Server import UDPServer
from PySocketLib.Client import ConnectedClient, ConnectedUDPClient
import socket
import datetime

class MyServer(UDPServer):
    def get_date(self):
        return str(datetime.datetime.now())

if __name__ == '__main__':
    server = MyServer(('localhost', 3000))
    
    while True:
        server.proceed()

        for msg in server.get_messages_from_clients():
            print(msg)
            server.send(msg.content, server.get_client_by_addr(msg.from_))

        server.clear_messages()