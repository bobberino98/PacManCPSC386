from pygame.sprite import Sprite
from imagerect import ImageRect
import pygame


class PacMan(Sprite):

    def __init__(self, screen, row, col, maze):
        super(PacMan, self).__init__()
        self.screen = screen
        self.im = ImageRect(screen, "pac_man_1", 18, 18)
        self.im.rect.centerx = col*10+5
        self.im.rect.centery = row*10+5
        self.maze = maze
        self.rect = self.im.rect
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False
        self.speed = 10
        self.state = 1
        self.death_state = 1
        self.dir = ""
        self.speed_timer = pygame.time.get_ticks()
        self.row = row
        self.col = col
        self.walls = ['T', 'B', 'R', 'L', 'G', 'M', 'N', 'O', 'Y', 'Z', 'W', 'X']
        self.dead = False

    def update(self):
        temp = ""
        if not self.dead:
            if self.moving_up and pygame.time.get_ticks() - self.speed_timer >= 100:

                temp = self.maze.rows[self.row-1]
                val = temp[self.col]
                if val not in self.walls:
                    self.im.rect.y -= self.speed
                    self.row -= 1
                self.im.blitme()
                self.speed_timer = pygame.time.get_ticks()
                self.dir = 'up'
                temp = "pac_man_up_" + str(self.state)
            elif self.moving_down and pygame.time.get_ticks() - self.speed_timer >= 100:
                temp = self.maze.rows[self.row+1]
                val = temp[self.col]
                if val not in self.walls:
                    self.row += 1
                    self.im.rect.y += self.speed
                self.im.blitme()
                self.speed_timer = pygame.time.get_ticks()
                self.dir = 'down'
                temp = "pac_man_down_" + str(self.state)
            elif self.moving_right and pygame.time.get_ticks() - self.speed_timer >= 100:

                temp = self.maze.rows[self.row]
                val = temp[self.col+1]
                if val not in self.walls:
                    self.im.rect.x += self.speed
                    self.col += 1
                self.im.blitme()
                self.speed_timer = pygame.time.get_ticks()
                self.dir = 'right'
                temp = "pac_man_right_" + str(self.state)
            elif self.moving_left and pygame.time.get_ticks() - self.speed_timer >= 100:
                temp = self.maze.rows[self.row]
                val = temp[self.col-1]
                if val not in self.walls:
                    self.im.rect.x -= self.speed
                    self.col -= 1
                self.im.blitme()
                self.speed_timer = pygame.time.get_ticks()
                self.dir = 'left'
                temp = "pac_man_left_" + str(self.state)
            else:
                return
            self.rect = self.im.rect
            self.im = ImageRect(self.screen, temp, 18, 18)
            self.im.rect = self.rect
            if self.state >= 3:
                self.state = 1
            else:
                self.state += 1
        else:
            if pygame.time.get_ticks() - self.speed_timer >= 200 and self.death_state < 12:
                temp = "pac_man_death_" +str(self.death_state)
                self.death_state += 1
                self.rect = self.im.rect
                self.im = ImageRect(self.screen, temp, 18, 18)
                self.im.rect = self.rect
                self.speed_timer = pygame.time.get_ticks()

    def blitme(self):
        self.im.blitme()
