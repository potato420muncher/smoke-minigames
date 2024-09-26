from .base_cs import BaseCs
import random

class ShuffledCs(BaseCs):
    def __init__(self):
        super().__init__()
        self.nb_shuffles = 0


    def update_game(self):
        super().update_game()

        if self.score == 3 :
            if self.nb_shuffles == 0:
                self.shuffle_colors()
            self.level = 2
        elif self.score == 20 :
            self.timer.setInterval(20)
            self.level = 3
        elif self.score == 30 :
            if self.nb_shuffles == 1:
                self.shuffle_colors()
            self.level = 4
        elif self.score == 40 :
            self.timer.setInterval(17)
            self.level = 5
        elif self.score == 50 :
            self.level = 6  
            self.game_over(True)


    def shuffle_colors(self) :
        random.shuffle(self.colors)

        self.update()

        self.nb_shuffles += 1