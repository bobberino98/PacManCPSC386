import os


class GameStats:

    def __init__(self):
        f = open('high_scores.txt', 'r')
        self.score = 0
        self.level = 1
        self.reset_stats()
        self.game_active = False
        self.show_high_score = False
        self.lives_left = 3
        if os.path.getsize("high_scores.txt") != 0:
            self.high_score = int(f.read())
        else:
            self.high_score = 0

    def write(self):
        f = open("high_scores.txt", 'w')
        f.write(str(self.high_score))

    def reset_stats(self):
        self.score = 0
        self.level = 1

    def check_high_score(self):

        if self.score > self.high_score:
            self.high_score = self.score
