import pygame as pg
from PySocketLib.Client import UDPClient

class GameClient(UDPClient):
    def on_receive(self, data: bytes):
        return data

    def on_send(self, data: bytes):
        return data

class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1920, 1080))
        self.clock = pg.time.Clock()

        self.player_cords = pg.math.Vector2(960, 540)
        
        self.client = GameClient(('127.0.0.1', 5000), 1024)

    def run(self):
        running = True

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.client.send(bytes(f'{self.player_cords.x};{self.player_cords.y}', encoding='utf-8'))
            self.screen.fill('black')

            for msg in self.client.get_messages_from_server():
                ...                

            pg.display.update()
            self.client.proceed()
            self.clock.tick(100)

if __name__ == "__main__":
    ...