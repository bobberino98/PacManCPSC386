from imagerect import ImageRect
from pygame.sprite import Sprite
import pygame


class Ghost(Sprite):

    def __init__(self, ghost_type, rect, p_man, screen, maze):
        super(Ghost, self).__init__()
        self.type = ghost_type
        self.p_man = p_man
        self.maze = maze
        if self.type == 'b':
            self.filename = "g_red_"
        elif self.type == 'p':
            self.filename = 'g_pink_'
        elif self.type == 'i':
            self.filename = 'g_teal_'
        elif self.type == 'c':
            self.filename = 'g_orng_'
        self.screen = screen
        self.rect = rect
        self.target = None
        self.speed = 8
        self.collide_right = False
        self.collide_left = False
        self.collide_up = False
        self.collide_down = False
        self.moving_right = False
        self.moving_left = True
        self.moving_up = False
        self.moving_down = False
        self.state = 1
        self.dir = 'left'
        self.im = ImageRect(self.screen, self.filename+self.dir+'_'+str(self.state), 25, 25)
        self.im.rect = rect
        self.timer = pygame.time.get_ticks()

    def move_left(self):
        if not self.collide_left:
            self.rect.x -= self.speed
            for brick in self.maze.bricks:
                if self.rect.colliderect(brick):
                    self.rect.x = brick.left - 1 - self.rect.width
                    self.collide_left = True
            self.dir = 'left'

    def move_right(self):
            if not self.collide_right:
                self.rect.x += self.speed
                for brick in self.maze.bricks:
                    if self.rect.colliderect(brick):
                        self.rect.x = brick.left - 1 - self.rect.width
                        self.collide_right = True
            self.dir = 'right'

    def move_up(self):
        if not self.collide_up:
            self.rect.y -= self.speed
            for brick in self.maze.bricks:
                if self.rect.colliderect(brick):
                    self.rect.y = brick.bottom + 1
                    self.collide_up = True
            self.dir = 'up'

    def move_down(self):
        if not self.collide_down:
            self.rect.y += self.speed
            for brick in self.maze.bricks:
                if self.rect.colliderect(brick):
                    self.rect.y = brick.top - 1 - self.rect.height
                    self.collide_down = True
            self.dir = 'down'

    def update(self):

        if self.type == 'b':
            self.target = self.p_man.rect

            for i in self.maze.intersections:
                if self.rect.colliderect(i):
                    if self.rect.x < self.target.x and i.right:
                        self.collide_right = False
                        self.moving_right = True
                        self.moving_left = False
                        self.moving_up = False
                        self.moving_down = False
                    elif self.rect.x > self.target.x and i.left:
                        self.collide_left = False
                        self.moving_right = False
                        self.moving_left = True
                        self.moving_up = False
                        self.moving_down = False
                    elif self.rect.y < self.target.y and i.down:
                        self.collide_down = False
                        self.moving_right = False
                        self.moving_left = False
                        self.moving_up = False
                        self.moving_down = True
                    elif self.rect.y > self.target.y and i.up:
                        self.collide_up = False
                        self.moving_right = False
                        self.moving_left = False
                        self.moving_up = True
                        self.moving_down = False
            if self.collide_right:
                if self.rect.y < self.target.y:
                    self.moving_right = False
                    self.moving_left = False
                    self.moving_up = False
                    self.moving_down = True
                elif self.rect.y > self.target.y:
                    self.moving_right = False
                    self.moving_left = False
                    self.moving_up = True
                    self.moving_down = False

        elif self.type == 'p':
            self.target = self.p_man.rect
            if self.p_man.moving_left:
                self.target.x -= 40
            elif self.p_man.moving_right:
                self.target.x += 40
            elif self.p_man.moving_down:
                self.target.y += 40
            elif self.p_man.moving_up:
                self.target.y -= 40
        # elif self.type == 'i':

        # elif self.type == 'c':
        #      self.target = self.game.p_man.rect
        #    if self.rect.x < self.target:
        if self.moving_left and not self.collide_left:
            self.move_left()
        elif self.moving_right and not self.collide_right:
            self.move_right()
        elif self.moving_up and not self.collide_up:
            self.move_up()
        elif self.moving_down and not self.collide_down:
            self.move_down()

        if self.state == 1:
            self.state = 2
        elif self.state == 2:
            self.state = 1
        self.im = ImageRect(self.screen, self.filename + self.dir + '_' + str(self.state), 25, 25)
        self.im.rect = self.rect
        self.im.blitme()
        self.timer = pygame.time.get_ticks()
