import socket
import pickle
import random

class SnakeServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432
        self.food_pos = []
        self.data_snake_1 = []
        self.data_snake_2 = []
    def Food(self):

        while not self.food_pos:
            x = random.randint(2, 28) * 20
            y = random.randint(2, 28) * 20
            if not [x, y] in self.data_snake_1 and not [x, y] in self.data_snake_2:
                self.food_pos = [x, y]
                self.data_snake_1.append(self.food_pos)
                self.data_snake_2.append(self.food_pos)
                break
        
                
        if self.data_snake_1[-2] == self.food_pos or self.data_snake_2[-2] == self.food_pos:
            self.food_pos = []
        if self.food_pos:
            self.data_snake_1.append(self.food_pos)
            self.data_snake_2.append(self.food_pos)
    def Start(self):
        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        # Port to listen on (non-privileged ports are > 1023)
        PORT = 65432

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind((HOST, PORT))
        s.listen(5)
        conn_list = []
        for i in range(2):
            conn, addr = s.accept()
            print('Connected by', addr)
            conn_list.append(conn)
        while True:

            self.data_snake_1 = conn_list[0].recv(1024)
            self.data_snake_2 = conn_list[1].recv(1024)
            if not self.data_snake_1:
                break
            if not self.data_snake_2:
                break
            
            self.data_snake_1 = pickle.loads(self.data_snake_1)
            self.data_snake_2 = pickle.loads(self.data_snake_2)

            self.Food()
            
            self.data_snake_1 = pickle.dumps(self.data_snake_1)
            self.data_snake_2 = pickle.dumps(self.data_snake_2)
            
            conn_list[0].sendall(self.data_snake_2)
            conn_list[1].sendall(self.data_snake_1)
SnakeServer().Start()
