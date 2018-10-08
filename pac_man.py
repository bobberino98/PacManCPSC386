import pygame
from imagerect import ImageRect

class PacMan:

    def __init__(self, screen):

        self.im = ImageRect(screen, "pac_man_1", 30, 30)
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False
        self.speed = 10

    def update(self):
        if self.moving_up:
            self.im.rect.y += self.speed
            self.im.blitme()