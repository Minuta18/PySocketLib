import socket

class Client:
    '''Simple socket client'''
    def __init__(self, 
        hostname: str='0.0.0.0', 
        port: int=8000,
    ):
        self.__hostname = hostname
        self.__port = port

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__hostname, self.__port))

    def __del__(self):
        self.__socket.close()

    def __service_connection(self):
        recv_data = self.__socket.recv(1024)
        self.on_receive(recv_data)

    def send(self, data: bytes):
        '''Actions to do when sending data'''
        self.__socket.sendall(bytes(data, encoding='utf-8'))
        return data

    def on_receive(self, data: bytes):
        '''Actions to do when receiving data'''
        return data
    
    def proceed(self):
        self.__service_connection()