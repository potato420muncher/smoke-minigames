import sys
import random

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer

from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 600)
        self.layout = QVBoxLayout(self)

        title_label = QLabel("Colorshifter")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

        play_button = QPushButton("Play Normal")
        play_button.clicked.connect(lambda: self.start_game(0))
        self.layout.addWidget(play_button)

        play_button_s = QPushButton("Play Shuffled")
        play_button_s.clicked.connect(lambda: self.start_game(1))
        self.layout.addWidget(play_button_s)

    def start_game(self, mode):
        self.game = Game(mode)
        self.clearFocus()
        self.game.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.game.setFocus()  # Set focus to game widget
        self.parent().setCentralWidget(self.game)  # Change central widget to game

    


class Game(QWidget):
    
    def __init__(self, gamemode):
        super().__init__()
        self.setFixedSize(400, 600)
        self.score = 0
        self.speed = 30
        self.level = 1
        self.mode = gamemode
        self.running = 0
        self.nb_shuffles = 0
        self.player_rect = QRect(175, 500, 50, 50)
        self.obstacles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)

        self.layout = QVBoxLayout(self)
        self.label = QLabel("Click to start game")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.score_label = QLabel("")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.score_label)

        # Colors
        self.color_blue = QColor(0,0,255)
        self.color_green = QColor(0,255,0)
        self.color_red = QColor(255,0,0)
        self.color_yellow = QColor(255,255,0)

        self.colors = [self.color_blue, self.color_green, self.color_red, self.color_yellow]

        self.blue_rect = QRect(25, 200, 50, 50)
        self.green_rect = QRect(125, 200, 50, 50)
        self.red_rect = QRect(225, 200, 50, 50)
        self.yellow_rect = QRect(325, 200, 50, 50)

        self.colors_rect = [self.blue_rect, self.green_rect, self.red_rect, self.yellow_rect]


        self.player_color = self.color_blue
        self.obstacle_color = self.color_blue

    def mousePressEvent(self, event) :
        if event.button() == Qt.MouseButton.LeftButton :

            if not self.running :
                print("mouse pressed")

                self.label.setText("")
                self.score_label.setText(str(self.score))
                self.timer.start(self.speed)
                self.running = 1

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

    def shuffle_colors(self) :
        random.shuffle(self.colors)

        self.update()

        self.nb_shuffles += 1


    def update_game(self):
        # Move obstacles and check for collisions
        for obstacle in self.obstacles:
            obstacle['rect'].moveLeft(obstacle['rect'].left() - 5)

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



        if self.mode == 0 :
            if self.score == 3 :
                self.timer.setInterval(27)
                self.level = 2
            elif self.score == 20 :
                self.timer.setInterval(25)
                self.level = 3
            elif self.score == 30 :
                self.timer.setInterval(20)
                self.level = 4
            elif self.score == 40 :
                self.timer.setInterval(15)
                self.level = 5
            elif self.score == 50 :
                self.level = 6  
                self.game_over(True)


        elif self.mode == 1 :
            if self.score == 3 :
                if self.mode == 1 and self.nb_shuffles == 0:
                    self.shuffle_colors()
                self.level = 2
            elif self.score == 20 :
                self.timer.setInterval(20)
                self.level = 3
            elif self.score == 30 :
                if self.mode == 1 and self.nb_shuffles == 1:
                    self.shuffle_colors()
                self.level = 4
            elif self.score == 40 :
                self.timer.setInterval(17)
                self.level = 5
            elif self.score == 50 :
                self.level = 6  
                self.game_over(True)
        

        for obstacle in self.obstacles:
            if self.player_rect.intersects(obstacle['rect']) and not self.player_color == self.obstacle_color:
                self.game_over(False)

        self.update()  # Repaint the game

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
        painter.setBrush(self.player_color)  # Player color
        painter.drawRect(self.player_rect.x(), self.player_rect.y() , self.player_rect.width(), self.player_rect.height())

        painter.setBrush(self.obstacle_color)  # Obstacle color
        for obstacle in self.obstacles:
            painter.drawRect(obstacle['rect'])

        for i in range(0,len(self.colors)) :
            painter.setBrush(self.colors[i])  # Obstacle color
            painter.drawRect(self.colors_rect[i].x(), self.colors_rect[i].y(), self.colors_rect[i].width(), self.colors_rect[i].height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()

    menu = Menu()

    window.setBaseSize(400, 600)
    window.setMaximumSize(400,600)
    window.setMinimumSize(400,600)
    window.setCentralWidget(menu)
    window.setWindowTitle("Colorshifter")

    app.setActiveWindow(window)

    window.show()
    sys.exit(app.exec())
