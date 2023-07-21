import PySocketLib
import base64
from PySocketLib.Client import ConnectedUDPClient
from PySocketLib.Server import UDPServer 
import pygame

game_clients = {}

class GameServer(UDPServer):
    def on_connect(self, client: ConnectedUDPClient):
        game_clients[client.addr] = [[0, 0], pygame.time.get_ticks()]

    def on_disconnect(self, client: ConnectedUDPClient):
        del game_clients[client.addr]

    def on_send(self, data: bytes) -> bytes:
        return data
    
    def on_receive(self, data: bytes) -> bytes:
        return data
    
if __name__ == '__main__':
    clock = pygame.time.Clock()
    server = UDPServer(('127.0.0.1', 5000))

    while True:
        server.proceed()

        for msg in server.get_messages_from_clients():
            client = game_clients[msg.from_]
            client[0] = msg.content

        raw_data = ''
        for client in server._clients.values():
            raw_data += ';'.join(game_clients[client.addr][0]) + '|'
        for client in server._clients.values():
            server.send(bytes(raw_data, encoding='utf-8'), server.get_client_by_addr(client[0]))

        for client in game_clients.values():
            if pygame.time.get_ticks() - client[1] >= 100:
                server._disconnect_client(server.get_client_by_addr(client[0]))

        clock.tick(100)