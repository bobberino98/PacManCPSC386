from imagerect import ImageRect
from pygame.sprite import Sprite
import pygame
from vector import Vec2d


class Ghost(Sprite):

    def __init__(self, ghost_type, p_man, screen, maze, row, col):
        super(Ghost, self).__init__()
        self.type = ghost_type
        self.p_man = p_man
        self.maze = maze
        self.row = row
        self.col = col
        if self.type == 'b':
            self.filename = "g_red_"
            self.targetcol = self.p_man.col
            self.targetrow = self.p_man.row
            self.nextrow = self.row
            self.nextcol = self.col - 1
        if self.type == 'p':
            self.filename = "g_pink_"
            self.targetcol = self.p_man.col + 4
            self.targetrow = self.p_man.row
            self.nextrow = self.row
            self.nextcol = self.col - 1
        elif self.type == 'p':
            self.filename = 'g_pink_'
        elif self.type == 'i':
            self.filename = 'g_teal_'
        elif self.type == 'c':
            self.filename = 'g_orng_'
        self.screen = screen
        self.target = None
        self.speed = 8
        self.collide_right = False
        self.collide_left = False
        self.collide_up = False
        self.collide_down = False

        self.state = 1
        self.dir = 'left'
        self.nextdir = 'left'
        self.im = ImageRect(self.screen, self.filename+self.dir+'_'+str(self.state), 18, 18)

        self.im.rect.centerx = col * 10 + 5
        self.im.rect.centery = row * 10 + 5
        self.rect = self.im.rect
        self.walls = ['T', 'B', 'R', 'L', 'G', 'M', 'N', 'O', 'Y', 'Z', 'W', 'X']
        self.timer = pygame.time.get_ticks()

    def update(self, move):

        if pygame.time.get_ticks() - self.timer >= 0:
            if move:
                self.col = self.nextcol
                self.row = self.nextrow
                self.dir = self.nextdir
            next_space = {}
            if self.dir == 'up':
                next_space = {'row': self.row - 1, 'col': self.col}
            elif self.dir == 'left':
                next_space = {'row': self.row, 'col': self.col - 1}
            elif self.dir == 'down':
                next_space = {'row': self.row + 1, 'col': self.col}
            elif self.dir == 'right':
                next_space = {'row': self.row, 'col': self.col + 1}

            adj_spaces = [{'row': next_space['row'] - 1, 'col': next_space['col'], 'dir': 'up'},
                          {'row': next_space['row'], 'col': next_space['col'] - 1, 'dir': 'left'},
                          {'row': next_space['row'] + 1, 'col': next_space['col'], 'dir': 'down'},
                          {'row': next_space['row'], 'col': next_space['col'] + 1, 'dir': 'right'}]
            behind = ''
            options = []
            if self.dir == 'left':
                behind = 'right'
            elif self.dir == 'right':
                behind = 'left'
            elif self.dir == 'up':
                behind = 'down'
            elif self.dir == 'down':
                behind = 'up'

            for space in adj_spaces:
                if space['dir'] == behind:
                    continue
                temp = self.maze.rows[space['row']]
                val = temp[space['col']]
                if val not in self.walls:
                    options.append(space)
                if len(options) > 1:
                    self.update_target()

                target = Vec2d(self.targetcol, self.targetrow)
                min_distance = 28*36
                for o in options:
                    opt_vec = Vec2d(o['col'], o['row'])
                    o['dist'] = opt_vec.get_distance(Vec2d(target))
                    if o['dist'] < min_distance:
                        self.nextdir = o['dir']
                        min_distance = o['dist']
                self.nextrow = next_space['row']
                self.nextcol = next_space['col']
                if self.state == 1:
                    self.state = 2
                elif self.state == 2:
                    self.state = 1
                self.im = ImageRect(self.screen, self.filename + self.dir + '_' + str(self.state), 18, 18)
                self.im.rect.centerx = self.col * 10 + 5
                self.im.rect.centery = self.row * 10 + 5
                self.rect = self.im.rect

            self.timer = pygame.time.get_ticks()

            self.im.blitme()

    def update_target(self):
        if self.type ==  'b':
            self.targetrow = self.p_man.row
            self.targetcol = self.p_man.col
        elif self.type == 'p':
            if self.p_man.dir == 'up':
                self.targetrow = self.p_man.row - 4
                self.targetcol = self.p_man.col - 4
            elif self.p_man.dir == 'down':
                self.targetrow = self.p_man.row + 4
                self.targetcol = self.p_man.col
            elif self.p_man.dir == 'left':
                self.targetcol = self.p_man.col - 4
                self.targetrow = self.p_man.row
            elif self.p_man.dir == 'right':
                self.targetcol = self.p_man.col + 4
                self.targetrow = self.p_man.row
            print(str(self.targetcol) + ' ' + str(self.targetrow))

    def blitme(self):
        self.im.blitme()
