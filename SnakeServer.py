import socket
import pickle
import random
import threading

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
    def GameSession(self, Connections):
        food_pos = []
        data_snake_1 = []
        data_snake_2 = []
        while True:

            data_snake_1 = Connections[0].recv(1024)
            data_snake_2 = Connections[1].recv(1024)
            if not data_snake_1:
                break
            if not data_snake_2:
                break
            
            data_snake_1 = pickle.loads(data_snake_1)
            data_snake_2 = pickle.loads(data_snake_2)

            while not food_pos:
                x = random.randint(2, 28) * 20
                y = random.randint(2, 28) * 20
                if not [x, y] in data_snake_1 and not [x, y] in data_snake_2:
                    food_pos = [x, y]
                    data_snake_1.append(food_pos)
                    data_snake_2.append(food_pos)
                    break
        
                
            if data_snake_1[-2] == food_pos or data_snake_2[-2] == food_pos:
                food_pos = []
            if food_pos:
                data_snake_1.append(food_pos)
                data_snake_2.append(food_pos)
                
            data_snake_1 = pickle.dumps(data_snake_1)
            data_snake_2 = pickle.dumps(data_snake_2)
            
            Connections[0].sendall(data_snake_2)
            Connections[1].sendall(data_snake_1)

    def Start(self):
        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        # Port to listen on (non-privileged ports are > 1023)
        PORT = 65432

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind((HOST, PORT))
        s.listen(5)
        conn_list = []
        threads = []
        while True:
            for i in range(2):
                conn, addr = s.accept()
                print('Connected by', addr)
                conn_list.append(conn)

            threads.append(threading.Thread(target=self.GameSession, args=(conn_list,)))
            threads[-1].start()
            conn_list = []    
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
