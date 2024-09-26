from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, QRect, Qt
from PyQt6.QtGui import QPainter, QColor
from games.menu import Menu
import random

class BaseCs(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 600)

        self.score = 0
        self.speed = 30
        self.level = 1
        self.running = False
        self.player_rect = QRect(175, 500, 50, 50)
        self.obstacles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(0)  # Remove spacing between widgets

        self.label = QLabel("Click to start game")
        self.label.setStyleSheet("color: white; font-size: 16px;")  # Text styling
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.score_label = QLabel("")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.score_label)


        self.blue_rect = QRect(25, 200, 50, 50)
        self.green_rect = QRect(125, 200, 50, 50)
        self.red_rect = QRect(225, 200, 50, 50)
        self.yellow_rect = QRect(325, 200, 50, 50)

        self.colors_rect = [self.blue_rect, self.green_rect, self.red_rect, self.yellow_rect]

        # Colors
        self.color_blue = QColor(0,0,255)
        self.color_green = QColor(0,255,0)
        self.color_red = QColor(255,0,0)
        self.color_yellow = QColor(255,255,0)

        self.colors = [self.color_blue, self.color_green, self.color_red, self.color_yellow]

        self.player_color = self.color_blue
        self.obstacle_color = self.color_blue

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.running:
            self.label.setText("")
            self.score_label.setText(str(self.score))
            self.timer.start(self.speed)
            self.running = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_H:
            self.player_color = self.colors[0]
        elif event.key() == Qt.Key.Key_J:
            self.player_color = self.colors[1]
        elif event.key() == Qt.Key.Key_K:
            self.player_color = self.colors[2]
        elif event.key() == Qt.Key.Key_L:
            self.player_color = self.colors[3]
        # Trigger a repaint after changing the color
        self.update()    

    def update_game(self):
        self.update()
        # Move obstacles and check for collisions
        for obstacle in self.obstacles:
            obstacle['rect'].moveLeft(obstacle['rect'].left() - 5)

        for obstacle in self.obstacles:
            if self.player_rect.intersects(obstacle['rect']) and not self.player_color == self.obstacle_color:
                self.game_over(False)

        # Remove obstacles that have gone off screen
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle['rect'].right() > 0]
        

        # Add new obstacles
        if len(self.obstacles) == 0:
            self.score_label.setText(str(self.score))

            # Generate new color
            col = random.randint(0,3)

            if self.score == 0 :
                col = 0

            if col == 0 :
                self.obstacle_color = self.color_blue
            elif col == 1 :
                self.obstacle_color = self.color_green
            elif col == 2 :
                self.obstacle_color = self.color_red
            else :
                self.obstacle_color = self.color_yellow

                
            new_obstacle = QRect(400, 500, 50, 50)
            self.obstacles.append({'rect': new_obstacle})
            self.score += 1



    def game_over(self, win):
        self.timer.stop()
        if win :
            print("Gagne! Bravo tu t'en tires sain et sobre")
        else :
            print("Perdu! Tu dois tirer", -(self.level)%6 , "taffes")

        self.clearFocus()

        self.menu = Menu()

        self.menu.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.menu.setFocus()  # Set focus to game widget
        self.parent().setCentralWidget(self.menu)  # Change central widget to game

    def paintEvent(self, event):
        painter = QPainter(self)

        # Fill the background with the current background color
        painter.fillRect(self.rect(), QColor(46, 46, 46))  # Match your dark grey

        painter.setBrush(self.player_color)  # Player color
        painter.drawRect(self.player_rect.x(), self.player_rect.y() , self.player_rect.width(), self.player_rect.height())

        painter.setBrush(self.obstacle_color)  # Obstacle color
        for obstacle in self.obstacles:
            painter.drawRect(obstacle['rect'])

        for i in range(0,len(self.colors)) :
            painter.setBrush(self.colors[i])  # Obstacle color
            painter.drawRect(self.colors_rect[i].x(), self.colors_rect[i].y(), self.colors_rect[i].width(), self.colors_rect[i].height())