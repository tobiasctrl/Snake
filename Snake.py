import pygame
import random
import socket
import pickle
import time

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class ClientGUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ClientGUI, self).__init__(*args, **kwargs)
        self._singleplayer = False
        self._online = False
        self.init_ui()
    def init_ui(self):
        self.setFixedHeight(250)
        self.setFixedWidth(300)
        self.setWindowTitle("Snake")

        self.sm = QLabel("Singleplayer/Multiplayer",self)
        self.sm.move(20,10)
        self.sm.resize(150,30)
        
        self.sm_radio_group = QButtonGroup(self)
        self.single_player  = QRadioButton('Singleplayer', self)
        self.single_player.move(20,30)
        self.sm_radio_group.addButton(self.single_player)

        self.multi_player = QRadioButton('Multiplayer', self)
        self.multi_player.move(120,30)
        self.sm_radio_group.addButton(self.multi_player)
        
        
        # self.online_local = QLabel("Online/Local",self)
        # self.online_local.move(20,60)
        
        # self.ol_radio_group = QButtonGroup(self)

        # self.online = QRadioButton('Online', self)
        # self.online.move(20,80)
        # self.ol_radio_group.addButton(self.online)        

        # self.local = QRadioButton("Local",self)
        # self.local.move(120,80)
        # self.ol_radio_group.addButton(self.local)
        
        
        self.online_multiplayer = QLabel("Multiplayer:", self)
        self.online_multiplayer.resize(130, 20)
        self.online_multiplayer.move(20, 80)
        

        self.port_label = QLabel("Port:",self)
        self.port_label.move(20,100)
        self.port_input = QLineEdit(self)
        self.port_input.move(50, 105)
        self.port_input.resize(50,20)
        self.port_input.setText("65432")

        self.ip_label = QLabel("IP:", self)
        self.ip_label.move(120, 100)
        self.ip_input = QLineEdit(self)
        self.ip_input.move(150, 105)
        self.ip_input.resize(120,20)

        self.start_session = QPushButton("Start", self)
        self.start_session.move(215,200)
        self.start_session.resize(70,40)

        
        # self.local.clicked.connect(self.on_Local)
        # self.local.click()

        self.single_player.clicked.connect(self.on_Singleplayer)
        self.single_player.click()

        self.multi_player.clicked.connect(self.on_Multiplayer)

        # self.online.clicked.connect(self.on_online)


        self.start_session.clicked.connect(self.on_start)
    def on_start(self):
        if self._singleplayer:
            Snake()
        else:
            if self._online:
                Snake(True,str(self.ip_input.text()),int(self.port_input.text()))
            else:
                Snake(True)
    # def on_online(self):
    #     self.port_input.setEnabled(True)
    #     self.ip_input.setEnabled(True)
    #     self._online = True
    # def on_Local(self):
    #     self.port_input.setEnabled(False)
    #     self.ip_input.setEnabled(False)
    #     self._online = False
    def on_Singleplayer(self):
        # self.online.setEnabled(False)
        # self.local.setEnabled(False)
        self.port_input.setEnabled(False)
        self.ip_input.setEnabled(False)
        self._singleplayer = True
    def on_Multiplayer(self):
        # self.online.setEnabled(True)
        # self.local.setEnabled(True)
        self.port_input.setEnabled(True)
        self.ip_input.setEnabled(True)
        self._singleplayer = False
        

class SnakeClient:
    def __init__(self,HOST='127.0.0.1', PORT=65432):

        self.HOST = HOST  
        self.PORT = PORT        

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Connect(self):
        self.s.connect((self.HOST, self.PORT))

    def Send(self, snake):
        data = pickle.dumps(snake)
        self.s.sendall(data)

    def Receive(self):
        data = self.s.recv(1024)
        enemy_snake = pickle.loads(data)
        return enemy_snake


class Snake():
    """
    Single/multiplayer Snake
    """

    def __init__(self, multiplayer=False, HOST='127.0.0.1', PORT=65432):
        super().__init__()
        self.multiplayer = multiplayer
        self.yellow = (255, 255, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.magenta = (255, 0, 255)
        self.cyan = (0, 255, 255)
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))

        pygame.display.set_caption('Snake')

        self.running = True
        self.food_pos = []
        self.direction = "Up"
        self.current_direction = self.direction

        if self.multiplayer:
            self.sc = SnakeClient(HOST, PORT)
            self.sc.Connect()
        self.enemy_snake = []
        self.snake = self.GetSpawnPos()
        self.GameLoop()

    def GetSpawnPos(self):
        x = 0
        y = 0
        not_in_other_snake = False
        while True:

            x = random.randint(3, 25) * 20
            y = random.randint(3, 26) * 20
            not_in_other_snake = True
            for yadd in range(0, 200, 20):
                if not not_in_other_snake:
                    break
                for xadd in range(0, 200, 20):
                    if (not [x + xadd, y + yadd] in self.enemy_snake and not [x - xadd, y - yadd] in self.enemy_snake and 
                    not [x + xadd, y - yadd] in self.enemy_snake and not [x - xadd, y + yadd] in self.enemy_snake):
                        pass
                    else:
                        not_in_other_snake = False
                        break
            if not_in_other_snake:
                break
        return [[x, y], [x+20, y]]

    def KeyPressed(self):
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_UP] and self.current_direction != "Down":
            self.direction = "Up"
        elif key_input[pygame.K_DOWN] and self.current_direction != "Up":
            self.direction = "Down"
        elif key_input[pygame.K_RIGHT] and self.current_direction != "Left":
            self.direction = "Right"
        elif key_input[pygame.K_LEFT] and self.current_direction != "Right":
            self.direction = "Left"

    def GameLoop(self):
        fps = 10
        frametime = 1/fps
        t = time.time()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.KeyPressed()
            if time.time() - t >= frametime:

                self.screen.fill((0, 0, 0))
                self.HeadPosition = self.snake[-1]
                self.MoveSnake()
                self.MapBorder()

                self.DrawSnake(self.snake, self.blue, self.yellow)
                if self.multiplayer:

                    self.sc.Send(self.snake)
                    self.enemy_snake = self.sc.Receive()
                    self.food_pos = self.enemy_snake[-1]
                    self.Food()
                    self.enemy_snake = self.enemy_snake[:-1]
                    self.DrawSnake(self.enemy_snake, self.magenta, self.cyan)
                else:
                    self.Food()
                self.GetTailHit()

                pygame.display.flip()
                t = time.time()

    def DrawSnake(self, snake, head_color, tail_color):
        for index, value in enumerate(snake):
            try:
                next_value = snake[index + 1]
                if next_value[0] > value[0]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] + 2, value[1] + 2, 20, 16))
                elif next_value[0] < value[0]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] - 2, value[1] + 2, 20, 16))
                elif next_value[1] > value[1]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] + 2, value[1] + 2, 16, 20))
                elif next_value[1] < value[1]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] + 2, value[1] - 2, 16, 20))
            except:
                pygame.draw.rect(self.screen, head_color,
                                 (value[0] + 2, value[1] + 2, 16, 16))

    def SnakeDead(self):
        self.snake = self.GetSpawnPos()

    def MapBorder(self):
        border_start = 0
        border_end = 580
        border_thickness = 20

        pygame.draw.rect(self.screen, self.green, (border_start,
                                                   border_start, border_end, border_thickness))
        pygame.draw.rect(self.screen, self.green, (border_start,
                                                   border_start, border_thickness, border_end))
        pygame.draw.rect(self.screen, self.green, (border_end,
                                                   border_start, border_thickness, border_end))
        pygame.draw.rect(self.screen, self.green, (border_start,
                                                   border_end, border_end + border_thickness, border_thickness))

        if not border_end > self.HeadPosition[1] > 0:
            self.SnakeDead()
        if not border_end > self.HeadPosition[0] > 0:
            self.SnakeDead()

    def MoveSnake(self):

        for index, value in enumerate(self.snake):
            try:
                self.snake[index] = [
                    int(self.snake[index + 1][0]), int(self.snake[index + 1][1])]
            except:
                if self.direction == "Down":
                    self.snake[index][1] += 20
                if self.direction == "Up":
                    self.snake[index][1] -= 20
                if self.direction == "Left":
                    self.snake[index][0] -= 20
                if self.direction == "Right":
                    self.snake[index][0] += 20
        self.current_direction = self.direction

    def Food(self):

        while not self.food_pos:
            x = random.randint(2, 28) * 20
            y = random.randint(2, 28) * 20
            if not [x, y] in self.snake:
                self.food_pos = [x, y]
        pygame.draw.rect(self.screen, self.red,
                         (self.food_pos[0] + 2, self.food_pos[1] + 2, 16, 16))

        if self.HeadPosition == self.food_pos:
            self.food_pos = []
            self.snake.insert(0, self.snake[0])

    def GetTailHit(self):
        if self.HeadPosition in self.snake[:-1] or self.HeadPosition in self.enemy_snake:
            self.SnakeDead()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_window = ClientGUI()
    client_window.show()
    app.exec_()
