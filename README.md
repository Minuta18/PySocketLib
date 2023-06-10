# Welcome to PySocketLib quick start

You will create simple echo-server

## Creating project

Create files with following structure:

```bash
.
├── Client
│   └── Main.py
└── Server
    └── Main.py
```

## Server

First, create class `EchoServer`, which is overloading `TCPServer`:

```python
from PySocketLib.Server import TCPServer
from PySocketLib.Client import ConnectedClient
import socket

class EchoServer(TCPServer):
    def connect_client(self):
        ...

    def disconnect_client(self):
        ...

    def on_receive(self):
        ...

    def on_send(self):
        ...

if __name__ == '__main__':
    server = EchoServer(('', 3000))
    
    while True:
        server.proceed()
```

Methods:
`connect_client` - Actions to do when client connects,
`disconnect_client` - Actions to do when client disconnects,
`on_receive` - Actions to do when server receives message from client,
`on_send` - Actions to do when server sends message to client,

Added some functionality:

```python
from PySocketLib.Server import TCPServer
from PySocketLib.Client import ConnectedClient
import socket

class EchoServer(TCPServer):
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
    server = EchoServer(('', 3000))
    
    while True:
        server.proceed()
```

## Client

Let's create simple client, which input something from user and send it to server:

```python
from PySocketLib.Client import Client

class MyClient(Client):
    def send(self, data: bytes):
        data = input('You: ')

        return super().send(data)
    
    def on_receive(self, data: bytes):
        print('Server: ' + str(data))

        return super().on_receive(data)
    
if __name__ == '__main__':
    cl = MyClient(('', 3000))
    while True:
        cl.send(b'')
        cl.proceed()
```

## Result

Server output:

```bash
[INFO] Connected client with address: ('127.0.0.1', 39652)
[INFO] Received b'Test message'
[INFO] Sent data b'Test message'
[INFO] Received b'1234'
[INFO] Sent data b'1234'
[INFO] Received b'Hi'
[INFO] Sent data b'Hi'
[INFO] Disconnect client with address: ('127.0.0.1', 39652)
^C
```

Client output:

```bash
You: Test message
Server: b'Test message'
You: 1234
Server: b'1234'
You: Hi
Server: b'Hi'
You: ^C
```
