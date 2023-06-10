from PySocketLib.Client import Client

class MyClient(Client):
    def send(self, data: bytes):
        data = input('You: ')

        return super().send(data)
    
    def on_receive(self, data: bytes):
        print('Server: ' + str(data))

        return super().on_receive(data)
    
if __name__ == '__main__':
    cl = MyClient(('', 3000, 0, 0))
    while True:
        cl.send(b'')
        cl.proceed()