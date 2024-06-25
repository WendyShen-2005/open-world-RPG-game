import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.18"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def get_pos(self):
        # print("hello " + pos)
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)  # try to connect to the client who is on the same address (player)
            return pickle.loads(self.client.recv(2048))  # get information that we the player send back
        except socket.error as e:
            print(e)
            print("did not connect")
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
