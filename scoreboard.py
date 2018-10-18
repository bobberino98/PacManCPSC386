import pygame.font
from pygame.sprite import Group
from pygame.sprite import Sprite
from imagerect import ImageRect


class Scoreboard:

    def __init__(self, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 20)

        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.bg_color)

        self.score_rect = self.score_image.get_rect()
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.bg_color)
        self.prep_score()
        self.prep_high_score()

        self.lives = Group()
        self.prep_lives()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.bg_color)
        self.score_rect.left = self.screen_rect.left
        self.score_rect.top = 0

    def prep_high_score(self):
        self.stats.check_high_score()
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.bg_color)
        self.high_score_rect.right = self.screen_rect.right
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.lives.draw(self.screen)

    def prep_lives(self):
        for x in range(self.stats.lives_left):
            temp = ImageRect(self.screen, "pac_man_right_1", 18, 18)
            life = Sprite()
            life.image = temp.image

            temp.rect.x = x * 18
            temp.rect.bottom = self.screen_rect.bottom - 1
            life.rect = temp.rect
            self.lives.add(life)
