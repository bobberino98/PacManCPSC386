from pygame.sprite import Sprite
from imagerect import ImageRect
import pygame


class PacMan(Sprite):

    def __init__(self, screen):
        super(PacMan, self).__init__()
        self.screen = screen
        self.im = ImageRect(screen, "pac_man_1", 25, 25)
        self.rect = self.im.rect
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False
        self.speed = 10
        self.state = 1
        self.dir = ""
        self.speed_timer = pygame.time.get_ticks()

    def update(self):
        temp = ""
        if self.moving_up and pygame.time.get_ticks() - self.speed_timer >= 100:
            self.im.rect.y -= self.speed
            self.im.blitme()
            self.speed_timer = pygame.time.get_ticks()
            temp = "pac_man_up_" + str(self.state)
        elif self.moving_down and pygame.time.get_ticks() - self.speed_timer >= 100:
            self.im.rect.y += self.speed
            self.im.blitme()
            self.speed_timer = pygame.time.get_ticks()
            temp = "pac_man_down_" + str(self.state)
        elif self.moving_right and pygame.time.get_ticks() - self.speed_timer >= 100:
            self.im.rect.x += self.speed
            self.im.blitme()
            self.speed_timer = pygame.time.get_ticks()
            temp = "pac_man_right_" + str(self.state)
        elif self.moving_left and pygame.time.get_ticks() - self.speed_timer >= 100:
            self.im.rect.x -= self.speed
            self.im.blitme()
            self.speed_timer = pygame.time.get_ticks()
            temp = "pac_man_left_" + str(self.state)
        else:
            return
        self.rect = self.im.rect
        self.im = ImageRect(self.screen, temp, 25, 25)
        self.im.rect = self.rect
        if self.state >= 3:
            self.state = 1
        else:
            self.state += 1

    def blitme(self):
        self.im.blitme()
