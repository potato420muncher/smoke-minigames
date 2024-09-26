from .base_cs import BaseCs
import random

class NormalCs(BaseCs):
    def __init__(self):
        super().__init__()
        # Additional initialization for the normal game

    def update_game(self):
        super().update_game()

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
