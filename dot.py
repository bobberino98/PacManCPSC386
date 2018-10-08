from pygame.sprite import Sprite
import pygame
from imagerect import ImageRect


class Dot(Sprite):

    def __init__(self, screen, rect):
        super(Dot, self).__init__()
        self.im = ImageRect(screen, "dot", 10, 10)
        self.screen = screen
        self.im.rect = rect

    def update(self):
        self.im.blitme()
