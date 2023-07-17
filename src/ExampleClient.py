from PySocketLib.Client import UDPClient

class MyClient(UDPClient):
    def on_receive(self, data: bytes):
        print('Server: ' + str(data))

        return super().on_receive(data)
    
if __name__ == '__main__':
    cl = MyClient(('127.0.0.1', 3000))
    while True:
        cl.send(bytes(input('You: '), encoding='utf-8'))
        cl.proceed()