import socket
import pickle


class SnakeServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432

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

            data_snake_1 = conn_list[0].recv(1024)
            data_snake_2 = conn_list[1].recv(1024)
            if not data_snake_1:
                break
            if not data_snake_2:
                break
            conn_list[0].sendall(data_snake_2)
            conn_list[1].sendall(data_snake_1)
            print(pickle.loads(data_snake_1))
            print(pickle.loads(data_snake_2))


SnakeServer().Start()
