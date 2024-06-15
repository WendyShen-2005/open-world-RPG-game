import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.17"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def get_pos(self):
        # print("hello " + pos)
        return self.pos

    def connect(self):
        print("he;;p")
        try:
            print("he")
            self.client.connect(self.addr)  # try to connect to the client who is on the same address (player)
            data = self.client.recv(2048).decode()
            print("connected : " + data)
            return data  # get information that we the player send back
        except socket.error as e:
            print(e)
            print("did not connect")
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
